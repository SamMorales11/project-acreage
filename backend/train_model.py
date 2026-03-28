import pandas as pd
import joblib
import os
import json
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Pastikan folder models ada
if not os.path.exists('models'):
    os.makedirs('models')

# 1. Dataset Sintetis
data = {
    'luas_tanah': [60, 72, 90, 120, 150, 200, 80, 100, 180, 250, 60, 75, 110, 140, 300, 45, 85, 130, 160, 220],
    'luas_bangunan': [45, 50, 70, 100, 120, 180, 60, 85, 150, 220, 40, 55, 90, 110, 250, 36, 65, 115, 140, 200],
    'kamar_tidur': [2, 2, 3, 3, 3, 4, 2, 3, 4, 5, 2, 2, 3, 3, 5, 1, 2, 3, 4, 5],
    'kamar_mandi': [1, 1, 2, 2, 2, 3, 1, 2, 3, 4, 1, 1, 2, 2, 4, 1, 1, 2, 2, 3],
    'lokasi_skor': [1, 1, 2, 2, 3, 3, 1, 2, 3, 3, 1, 1, 2, 2, 3, 1, 2, 2, 3, 3],
    'harga': [450, 550, 750, 1100, 1400, 2100, 600, 900, 1800, 2800, 420, 580, 1000, 1250, 3500, 350, 700, 1200, 1600, 2400]
}

df = pd.DataFrame(data)

# 2. Split Data (Training 80% & Testing 20%)
X = df.drop('harga', axis=1)
y = df['harga']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Training Model pada Data Latih
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 4. Evaluasi Akademis pada Data Uji (Testing)
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

# Format metrik ke dalam dictionary
metrics = {
    "mae": round(mae, 2),
    "rmse": round(rmse, 2),
    "r2": round(r2, 4)
}

# 5. Simpan Model & Metrik ke folder models/
joblib.dump(model, 'models/rf_model.joblib')

with open('models/metrics.json', 'w') as f:
    json.dump(metrics, f)

# 6. Simpan Feature Importance untuk Chart
importance = dict(zip(X.columns, model.feature_importances_))
joblib.dump(importance, 'models/feature_importance.joblib')

print("✅ Model training selesai.")
print(f"📊 Metrik Evaluasi -> MAE: {metrics['mae']}, RMSE: {metrics['rmse']}, R2: {metrics['r2']}")
print("✅ File rf_model.joblib & metrics.json berhasil dibuat di folder models/")