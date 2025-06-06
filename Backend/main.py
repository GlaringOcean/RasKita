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

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Pet Breed Prediction API", version="1.0.0")

# More specific CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=False,  # Must be False if using "*"
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add OPTIONS handler for preflight requests
@app.options("/predict")
async def options_predict():
    return JSONResponse(
        content={"message": "OK"}, 
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "*",
        }
    )

# --- Configuration and Initialization ---
MODEL_PATH = "./best_model.pth"
BREED_DESCRIPTIONS_URL = "https://docs.google.com/spreadsheets/d/1v9o-KPbQUnaWb9qK2hZfAHgOLrve4BKx1k30RUIYM3M/export?format=csv"

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
logger.info(f"Using device: {device}")

NUM_CLASSES = 55

model = None
class_names = [
    'Abyssinian', 'Alaskan Malamute', 'American Bobtail', 'American Shorhair', 'American bulldog',
    'American Pit Bull Terrier', 'Basset_hound', 'Beagle', 'Bengal', 'Birman', 'Bombay', 'Boxer',
    'British Shorthair', 'Bulldog', 'Calico', 'Chihuahua', 'Dachshund', 'Egyptian Mau',
    'English Cockerc Paniel', 'English Setter', 'German Shepherd', 'German Shorthairaired',
    'Golden Retreiver', 'Great Pyrenees', 'Havanese', 'Husky', 'Japanese Chin', 'Keeshond',
    'Labrador Retriever', 'Leonberger', 'Maine Coon', 'Miniature Pinscher', 'Munchkin',
    'Newfoundland', 'Norwegian Forest Cat', 'Ocicat', 'Persian', 'Pomeranian', 'Poodle', 'Pug',
    'Ragdoll', 'Rottweiler', 'Russian Blue', 'Saint Bernard', 'Samoyed', 'Scottish Fold',
    'Scottish Terrier', 'Shiba Inu', 'Siamese', 'Sphynx', 'Staffordshire Bull Terrier',
    'Tortoiseshell', 'Tuxedo', 'Wheaten Tersier', 'Yorkshire Terrier'
]

breed_descriptions_df = pd.DataFrame()

# Image transformations (must match your training)
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

def load_model():
    global model
    try:
        logger.info(f"Loading model from {MODEL_PATH}")
        model = models.efficientnet_b0(pretrained=False)
        num_ftrs: int = model.classifier[1].in_features  # type: ignore
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
        logger.info(f"Model loaded successfully from {MODEL_PATH}")
    except FileNotFoundError:
        logger.error(f"Model file not found at {MODEL_PATH}")
        raise RuntimeError(f"Model file not found at {MODEL_PATH}")
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        raise RuntimeError(f"Error loading model: {e}")

def load_breed_descriptions():
    global breed_descriptions_df
    try:
        logger.info("Loading breed descriptions...")
        response = requests.get(BREED_DESCRIPTIONS_URL, timeout=10)
        response.raise_for_status()
        from io import StringIO
        csv_data = StringIO(response.text)
        breed_descriptions_df = pd.read_csv(csv_data)
        logger.info(f"Loaded breed descriptions with columns: {breed_descriptions_df.columns.tolist()}")
    except Exception as e:
        logger.warning(f"Error loading breed descriptions: {e}")
        breed_descriptions_df = pd.DataFrame()

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up Pet Breed Prediction API...")
    load_model()
    load_breed_descriptions()
    logger.info("Startup complete!")

def get_breed_description(breed_name: str) -> str:
    if breed_descriptions_df.empty or breed_descriptions_df.shape[1] < 2:
        return "Description not available."

    breed_col = breed_descriptions_df.columns[0]
    row = breed_descriptions_df[
        breed_descriptions_df[breed_col].astype(str).str.strip().str.lower() == breed_name.strip().lower()
    ]

    if not row.empty:
        # Ambil kolom ke 1 sampai ke 6 (maksimum)
        max_index = min(6, breed_descriptions_df.shape[1] - 1)
        return '\n'.join(str(row.iloc[0, i]) for i in range(1, max_index + 1))

    return "Description not available."

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    logger.info(f"Received prediction request for file: {file.filename}")
    
    # Validate content type
    if not file.content_type or not file.content_type.startswith("image/"):
        logger.warning(f"Invalid content type: {file.content_type}")
        raise HTTPException(status_code=400, detail="File must be an image.")

    # Read file contents
    try:
        contents = await file.read()
        logger.info(f"File size: {len(contents)} bytes")
    except Exception as e:
        logger.error(f"Error reading file: {e}")
        raise HTTPException(status_code=400, detail="Error reading uploaded file.")

    # Process image
    try:
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        logger.info(f"Image size: {image.size}")
    except Exception as e:
        logger.error(f"Error processing image: {e}")
        raise HTTPException(status_code=400, detail="Invalid image file. Please provide a valid image (e.g., JPG, PNG).")

    # Check if model is loaded
    if model is None:
        logger.error("Model not loaded")
        raise HTTPException(status_code=500, detail="Model not loaded. Please try again later or check server logs.")

    # Make prediction
    try:
        input_tensor = cast(torch.Tensor, transform(image)).unsqueeze(0).to(device)
        logger.info(f"Input tensor shape: {input_tensor.shape}")

        with torch.no_grad():
            outputs = model(input_tensor)
            probabilities = torch.nn.functional.softmax(outputs, dim=1).squeeze(dim=0)
            top3_prob, top3_idx = torch.topk(probabilities, 3)

        results = []
        for prob, idx in zip(top3_prob, top3_idx):
            breed = class_names[int(idx.item())]
            description = get_breed_description(breed)
            results.append({
                "breed": breed,
                "confidence": f"{prob.item()*100:.2f}%",
                "description": description
            })

        confidence_message = None
        if top3_prob[0].item() < 0.70:
            confidence_message = "**Pesan: Pastikan gambar jelas! Konfidensi rendah.**"

        logger.info(f"Prediction successful. Top breed: {results[0]['breed']} ({results[0]['confidence']})")

        return JSONResponse(content={
            "predictions": results,
            "confidence_message": confidence_message
        })

    except Exception as e:
        logger.error(f"Error during prediction: {e}")
        raise HTTPException(status_code=500, detail="Error during prediction. Please try again.")

@app.get("/")
async def root():
    return {
        "message": "Welcome to the Pet Breed Prediction API!",
        "status": "running",
        "model_loaded": model is not None,
        "device": str(device)
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "device": str(device),
        "breed_descriptions_loaded": not breed_descriptions_df.empty
    }

if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting server...")
    # Run the server on all network interfaces (0.0.0.0) so other devices can connect
    uvicorn.run(
        "main:app",  # Replace "main" with your actual filename if different
        host="0.0.0.0",  # This allows external connections
        port=7860,
        reload=True,  # Remove this in production
        log_level="info"
    )