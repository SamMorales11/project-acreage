import axios from 'axios';

// Ganti URL ini setelah Anda mendapatkan domain dari Render/Railway
const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export default {
  predictPrice(data) { return apiClient.post('/predict', data); },
  getAnalytics() { return apiClient.get('/analytics/features'); },
};