import axios from 'axios';

const apiClient = axios.create({
  // URL ini mengarah langsung ke server Hugging Face Anda
  baseURL: 'https://semskii1-acreage-api.hf.space', 
  headers: {
    'Content-Type': 'application/json',
  },
});

export default {
  predictPrice(data) { return apiClient.post('/predict', data); },
  getAnalytics() { return apiClient.get('/analytics/features'); },
};