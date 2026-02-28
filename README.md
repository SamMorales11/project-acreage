# 🏠 Acreage: Real Estate Analytics & Price Prediction

Acreage adalah platform analitik properti *end-to-end* yang dirancang untuk memberikan estimasi harga hunian secara akurat menggunakan algoritma Machine Learning. Proyek ini menggabungkan kekuatan **Random Forest Regressor** untuk pemodelan prediktif dan **Vue.js** untuk antarmuka dashboard yang modern dan responsif.

---

## 🚀 Fitur Utama

- **Smart Price Prediction**: Estimasi harga rumah secara *real-time* berdasarkan spesifikasi (Luas Tanah, Bangunan, Kamar, & Lokasi).
- **Interactive Analytics Dashboard**: Visualisasi data fitur yang paling berpengaruh terhadap harga menggunakan Chart.js/ECharts.
- **Explainable AI (XAI)**: Menampilkan *Feature Importance* dari model Random Forest agar pengguna memahami variabel penentu harga.
- **Modern UI/UX**: Antarmuka bersih, minimalis, dan *mobile-friendly* yang dibangun dengan Tailwind CSS.
- **FastAPI Backend**: REST API yang efisien dengan dokumentasi Swagger otomatis.

---

## 🛠️ Tech Stack

### Data Science & Machine Learning
- **Python**: Bahasa pemrograman utama.
- **Scikit-Learn**: Untuk implementasi algoritma **Random Forest Regressor**.
- **Pandas**: Manipulasi dan pemrosesan dataset.
- **Joblib**: Untuk serialisasi dan pemuatan model ML.

### Backend (API)
- **FastAPI**: Framework web berperforma tinggi untuk melayani prediksi model.
- **Pydantic**: Validasi data input/output.
- **Uvicorn**: ASGI server untuk deployment.

### Frontend
- **Vue.js 3**: Progressive framework untuk antarmuka pengguna.
- **Tailwind CSS**: Framework CSS untuk styling yang cepat dan responsif.
- **Chart.js / ECharts**: Untuk visualisasi metrik data properti.

---

## 📂 Struktur Proyek

```text
acreage/
├── backend/            # FastAPI & Machine Learning Logic
│   ├── app/            # Source code API
│   ├── models/         # Pre-trained ML models (.joblib)
│   └── train_model.py  # Script untuk melatih model
├── frontend/           # Vue.js + Tailwind UI
└── README.md
