import pandas as pd
import joblib
import os
from sklearn.ensemble import RandomForestRegressor

# Pastikan folder models ada
if not os.path.exists('models'):
    os.makedirs('models')

# 1. Dataset Sintetis (Sesuai diskusi awal)
data = {
    'luas_tanah': [60, 72, 90, 120, 150, 200, 80, 100, 180, 250, 60, 75, 110, 140, 300, 45, 85, 130, 160, 220],
    'luas_bangunan': [45, 50, 70, 100, 120, 180, 60, 85, 150, 220, 40, 55, 90, 110, 250, 36, 65, 115, 140, 200],
    'kamar_tidur': [2, 2, 3, 3, 3, 4, 2, 3, 4, 5, 2, 2, 3, 3, 5, 1, 2, 3, 4, 5],
    'kamar_mandi': [1, 1, 2, 2, 2, 3, 1, 2, 3, 4, 1, 1, 2, 2, 4, 1, 1, 2, 2, 3],
    'lokasi_skor': [1, 1, 2, 2, 3, 3, 1, 2, 3, 3, 1, 1, 2, 2, 3, 1, 2, 2, 3, 3],
    'harga': [450, 550, 750, 1100, 1400, 2100, 600, 900, 1800, 2800, 420, 580, 1000, 1250, 3500, 350, 700, 1200, 1600, 2400]
}

df = pd.DataFrame(data)

# 2. Training Model
X = df.drop('harga', axis=1)
y = df['harga']

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# 3. Simpan Model ke folder models/
joblib.dump(model, 'models/rf_model.joblib')

# 4. Simpan Feature Importance untuk Chart
importance = dict(zip(X.columns, model.feature_importances_))
joblib.dump(importance, 'models/feature_importance.joblib')

print("✅ Model training selesai. File .joblib berhasil dibuat di folder models/")