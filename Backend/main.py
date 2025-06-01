from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import torch
from torchvision import transforms, models
import torch.nn as nn
from PIL import Image
import io
import pandas as pd
import os
import requests
from typing import cast
import logging

# --- Logger Setup ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Configuration ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "best_model.pth")
BREED_CSV_URL = "https://docs.google.com/spreadsheets/d/1v9o-KPbQUnaWb9qK2hZfAHgOLrve4BKx1k30RUIYM3M/export?format=csv"
NUM_CLASSES = 55
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# --- Class Names ---
class_names = [
    'Abyssinian', 'Alaskan_Malamute', 'American_Bobtail', 'American_Shorthair', 'American_bulldog',
    'American_pit_bull_terrier', 'Basset_hound', 'Beagle', 'Bengal', 'Birman', 'Bombay', 'Boxer',
    'British_shorthair', 'Bulldog', 'Calico', 'Chihuahua', 'Dachshund', 'Egyptian_mau',
    'English_cocker_spaniel', 'English_setter', 'German_Shepherd', 'German_shorthair_pointer',
    'Golden_Retriever', 'Great_pyrenees', 'Havanese', 'Husky', 'Japanese_chin', 'Keeshond',
    'Labrador_Retriever', 'Leonberger', 'Maine_coon', 'Miniature_pinscher', 'Munchkin',
    'Newfoundland', 'Norwegian_Forest_Cat', 'Ocicat', 'Persian', 'Pomeranian', 'Poodle', 'Pug',
    'Ragdoll', 'Rottweiler', 'Russian_blue', 'Saint_bernard', 'Samoyed', 'Scottish_Fold',
    'Scottish_terrier', 'Shiba_inu', 'Siamese', 'Sphynx', 'Staffordshire_bull_terrier',
    'Tortoiseshell', 'Tuxedo', 'Wheaten_terrier', 'Yorkshire_terrier'
]

# --- Transforms ---
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

model = None
breed_descriptions_df = pd.DataFrame()


# --- Model Loader ---
def load_model():
    global model
    try:
        model = models.efficientnet_b0(pretrained=False)
        num_ftrs = model.classifier[1].in_features
        model.classifier = nn.Sequential(
            nn.Dropout(0.3),
            nn.Linear(num_ftrs, 256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, NUM_CLASSES)
        )
        state_dict = torch.load(MODEL_PATH, map_location=device)
        model.load_state_dict(state_dict)
        model.to(device)
        model.eval()
        logger.info(f"✅ Model loaded from {MODEL_PATH}")
    except Exception as e:
        logger.error(f"❌ Failed to load model: {e}")
        raise RuntimeError("Model load failed.")


# --- CSV Descriptions Loader ---
def load_breed_descriptions():
    global breed_descriptions_df
    try:
        response = requests.get(BREED_CSV_URL)
        response.raise_for_status()
        from io import StringIO
        breed_descriptions_df = pd.read_csv(StringIO(response.text))

        if 'Breed' not in breed_descriptions_df.columns or 'Description' not in breed_descriptions_df.columns:
            logger.warning("❗ CSV missing required columns. Using empty descriptions.")
            breed_descriptions_df = pd.DataFrame(columns=['Breed', 'Description'])
        logger.info(f"✅ Loaded {len(breed_descriptions_df)} breed descriptions.")
    except Exception as e:
        logger.error(f"❌ Failed to load breed descriptions: {e}")
        breed_descriptions_df = pd.DataFrame(columns=['Breed', 'Description'])


# --- Startup Events ---
@app.on_event("startup")
async def startup_event():
    load_model()
    load_breed_descriptions()


# --- Description Lookup ---
def get_breed_description(breed_name: str) -> str:
    if breed_descriptions_df.empty:
        return "Description not available."
    row = breed_descriptions_df[
        breed_descriptions_df['Breed'].str.strip().str.lower() == breed_name.strip().lower()
    ]
    if not row.empty:
        return row.iloc[0]['Description']
    return "Description not available."


# --- Prediction Endpoint ---
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image.")

    contents = await file.read()
    try:
        image = Image.open(io.BytesIO(contents)).convert("RGB")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid image file. Use JPG/PNG.")

    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded.")

    input_tensor = cast(torch.Tensor, transform(image)).unsqueeze(0).to(device)

    with torch.no_grad():
        outputs = model(input_tensor)
        probabilities = torch.nn.functional.softmax(outputs, dim=1).squeeze(0)
        top3_prob, top3_idx = torch.topk(probabilities, 3)

    results = []
    for prob, idx in zip(top3_prob, top3_idx):
        breed = class_names[int(idx)]
        description = get_breed_description(breed)
        results.append({
            "breed": breed,
            "confidence": f"{prob.item()*100:.2f}%",
            "description": description
        })

    top_conf = top3_prob[0].item()
    confidence_message = None
    if top_conf < 0.70:
        confidence_message = "**Pesan: Pastikan gambar jelas! Konfidensi rendah.**"

    return JSONResponse(content={
        "predictions": results,
        "confidence_message": confidence_message
    })


# --- Root Endpoint ---
@app.get("/")
async def root():
    return {"message": "Welcome to the Pet Breed Prediction API!"}
