import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000', // URL default FastAPI
  headers: {
    'Content-Type': 'application/json',
  },
});

export default {
  predictPrice(data) {
    return apiClient.post('/predict', data);
  },
  getAnalytics() {
    return apiClient.get('/analytics/features');
  },
};