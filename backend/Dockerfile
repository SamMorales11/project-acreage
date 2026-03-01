# Menggunakan environment Python versi ringan
FROM python:3.10-slim

# Menentukan direktori kerja di dalam server
WORKDIR /app

# Menyalin file requirements dan menginstalnya
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Menyalin seluruh kode backend ke dalam server
COPY . .

# Mengekspos port 7860 (Port wajib untuk Hugging Face Spaces)
EXPOSE 7860

# Perintah untuk menjalankan server FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]