from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import torch
from torchvision import transforms, models
import torch.nn as nn
from PIL import Image
import io
import pandas as pd
import sqlite3
import os
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
DATABASE_PATH = "./petdatabase.db"  # Updated path to SQLite database file

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
logger.info(f"Using device: {device}")

NUM_CLASSES = 55

model = None
class_names = [
    'Abyssinian', 'Alaskan Malamute', 'American Bobtail', 'American Shorhair', 'American bulldog',
    'American Pit Bull Terrier', 'Basset Hound', 'Beagle', 'Bengal', 'Birman', 'Bombay', 'Boxer',
    'British Shorthair', 'Bulldog', 'Calico', 'Chihuahua', 'Dachshund', 'Egyptian Mau',
    'English Cocker Spaniel', 'English Setter', 'German Shepherd', 'German Shorthaired Pointer',
    'Golden Retreiver', 'Great Pyrenees', 'Havanese', 'Husky', 'Japanese Chin', 'Keeshond',
    'Labrador Retriever', 'Leonberger', 'Maine Coon', 'Miniature Pinscher', 'Munchkin',
    'Newfoundland', 'Norwegian Forest', 'Ocicat', 'Persian', 'Pomeranian', 'Poodle', 'Pug',
    'Ragdoll', 'Rottweiler', 'Russian Blue', 'Saint Bernard', 'Samoyed', 'Scottish Fold',
    'Scottish Terrier', 'Shiba Inu', 'Siamese', 'Sphynx', 'Staffordshire Bull Terrier',
    'Tortoiseshell', 'Tuxedo', 'Wheaten Terrier', 'Yorkshire Terrier'
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
        logger.info(f"Loading breed descriptions from database: {DATABASE_PATH}")

        if not os.path.exists(DATABASE_PATH):
            logger.error(f"Database file not found at {DATABASE_PATH}")
            breed_descriptions_df = pd.DataFrame()
            return

        conn = sqlite3.connect(DATABASE_PATH)

        # Load catbreeds and dogbreeds tables and combine
        catbreeds_df = pd.DataFrame()
        dogbreeds_df = pd.DataFrame()

        try:
            catbreeds_df = pd.read_sql_query("SELECT * FROM catbreeds", conn)
            logger.info(f"Loaded {len(catbreeds_df)} records from catbreeds")
        except Exception as e:
            logger.warning(f"Failed to load catbreeds table: {e}")

        try:
            dogbreeds_df = pd.read_sql_query("SELECT * FROM dogbreeds", conn)
            logger.info(f"Loaded {len(dogbreeds_df)} records from dogbreeds")
        except Exception as e:
            logger.warning(f"Failed to load dogbreeds table: {e}")

        # Combine dataframes vertically, adding a column to identify type
        catbreeds_df['type'] = 'cat'
        dogbreeds_df['type'] = 'dog'

        breed_descriptions_df = pd.concat([catbreeds_df, dogbreeds_df], ignore_index=True, sort=False)

        conn.close()

        if breed_descriptions_df.empty:
            logger.warning("No breed descriptions loaded from database")

    except Exception as e:
        logger.error(f"Error loading breed descriptions from database: {e}")
        breed_descriptions_df = pd.DataFrame()

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up Pet Breed Prediction API...")
    load_model()
    load_breed_descriptions()
    logger.info("Startup complete!")

def get_breed_description(breed_name: str) -> dict:
    if breed_descriptions_df.empty:
        return {}

    breed_col = 'breed_name'

    row = breed_descriptions_df[
        breed_descriptions_df[breed_col].astype(str).str.strip().str.lower() == breed_name.strip().lower()
    ]

    if not row.empty:
        # Return the entire row as a dictionary (first match)
        return row.iloc[0].to_dict()

    return {}

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
            breed_info = get_breed_description(breed)
            results.append({
                "breed": breed,
                "confidence": f"{prob.item()*100:.2f}%",
                "breed_name": breed_info.get('breed_name', breed),
                "height_male_min": breed_info.get('height_male_min'),
                "height_male_max": breed_info.get('height_male_max'),
                "height_female_min": breed_info.get('height_female_min'),
                "height_female_max": breed_info.get('height_female_max'),
                "weight_male_min": breed_info.get('weight_male_min'),
                "weight_male_max": breed_info.get('weight_male_max'),
                "weight_female_min": breed_info.get('weight_female_min'),
                "weight_female_max": breed_info.get('weight_female_max'),
                "life_expectancy_min": breed_info.get('life_expectancy_min'),
                "life_expectancy_max": breed_info.get('life_expectancy_max'),
                "characteristics": breed_info.get('characteristics'),
                "exercise_needs": breed_info.get('exercise_needs'),
                "grooming_requirements": breed_info.get('grooming_requirements'),
                "health_considerations": breed_info.get('health_considerations'),
                "diet_nutrition": breed_info.get('diet_nutrition')
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
        "breed_descriptions_loaded": not breed_descriptions_df.empty,
        "database_path": DATABASE_PATH,
        "database_exists": os.path.exists(DATABASE_PATH)
    }

# New endpoint to check database structure
@app.get("/database-info")
async def database_info():
    try:
        if not os.path.exists(DATABASE_PATH):
            return {"error": "Database file not found"}
        
        conn = sqlite3.connect(DATABASE_PATH)
        
        # Get table names
        tables_query = "SELECT name FROM sqlite_master WHERE type='table'"
        tables_df = pd.read_sql_query(tables_query, conn)
        tables = tables_df['name'].tolist()
        
        # Get column info for each table
        table_info = {}
        for table in tables:
            try:
                columns_query = f"PRAGMA table_info({table})"
                columns_df = pd.read_sql_query(columns_query, conn)
                table_info[table] = columns_df.to_dict('records')
            except Exception as e:
                table_info[table] = f"Error: {e}"
        
        conn.close()
        
        return {
            "database_path": DATABASE_PATH,
            "tables": tables,
            "table_info": table_info,
            "breed_descriptions_loaded": not breed_descriptions_df.empty
        }
        
    except Exception as e:
        return {"error": f"Error reading database: {e}"}

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