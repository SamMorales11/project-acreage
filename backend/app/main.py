from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import os
import json
import numpy as np

app = FastAPI()

# Wajib untuk koneksi Vue ke FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup Path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(os.path.dirname(BASE_DIR), "models", "rf_model.joblib")
METRICS_PATH = os.path.join(os.path.dirname(BASE_DIR), "models", "metrics.json")

# Muat model saat startup
try:
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
        print(f"✅ Model loaded successfully from {MODEL_PATH}")
    else:
        model = None
        print(f"❌ Model file NOT FOUND at {MODEL_PATH}")
except Exception as e:
    model = None
    print(f"❌ Error loading model: {str(e)}")

class PropertyInput(BaseModel):
    luas_tanah: float
    luas_bangunan: float
    kamar_tidur: float
    kamar_mandi: float
    lokasi_skor: float

@app.post("/predict")
async def predict(data: PropertyInput):
    if model is None:
        raise HTTPException(status_code=500, detail="Machine Learning model is not loaded on server.")
    
    try:
        input_data = np.array([[
            data.luas_tanah, 
            data.luas_bangunan, 
            data.kamar_tidur, 
            data.kamar_mandi, 
            data.lokasi_skor
        ]])
        
        prediction = model.predict(input_data)
        return {"estimasi_harga": round(float(prediction[0]), 2)}
    except Exception as e:
        print(f"❌ Prediction Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Error during model prediction process.")

@app.get("/analytics/features")
async def get_features():
    return {"labels": ["Luas Tanah", "Luas Bangunan", "Kamar Tidur", "Kamar Mandi", "Lokasi"], 
            "values": [35, 30, 10, 5, 20]}

# 🌟 ENDPOINT BARU UNTUK EVALUASI MODEL 🌟
@app.get("/analytics/metrics")
async def get_metrics():
    if os.path.exists(METRICS_PATH):
        with open(METRICS_PATH, "r") as f:
            metrics = json.load(f)
        return metrics
    else:
        # Kembalikan nilai 0 jika file belum ada
        return {"mae": 0, "rmse": 0, "r2": 0}