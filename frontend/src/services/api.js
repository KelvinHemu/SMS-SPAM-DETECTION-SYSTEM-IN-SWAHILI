import axios from 'axios';

const API_BASE_URL = 'http://localhost:3000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`🚀 API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('❌ API Request Error:', error);
    return Promise.reject(error);
  }
);

// Add response interceptor for logging
api.interceptors.response.use(
  (response) => {
    console.log(`✅ API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error('❌ API Response Error:', error.response?.status, error.response?.data);
    return Promise.reject(error);
  }
);

export const spamDetectionAPI = {
  // Analyze message
  analyzeMessage: async (senderPhone, receiverPhone, messageText) => {
    try {
      const response = await api.post('/analyze', {
        text: messageText,
        sender_phone: senderPhone,
        receiver_phone: receiverPhone
      });
      return response.data;
    } catch (error) {
      console.error('Error analyzing message:', error);
      throw error;
    }
  },

  // Get delivery statistics
  getDeliveryStats: async () => {
    try {
      const response = await api.get('/analyze/stats/delivery');
      return response.data;
    } catch (error) {
      console.error('Error fetching delivery stats:', error);
      throw error;
    }
  },

  // Get system health
  getHealthStatus: async () => {
    try {
      const response = await api.get('/health');
      return response.data;
    } catch (error) {
      console.error('Error fetching health status:', error);
      throw error;
    }
  },

  // Test endpoint
  testAnalysis: async () => {
    try {
      const response = await api.get('/analyze/test');
      return response.data;
    } catch (error) {
      console.error('Error testing analysis:', error);
      throw error;
    }
  },

  // Get Swahili labels
  getSwahiliLabels: async () => {
    try {
      const response = await api.get('/analyze/labels');
      return response.data;
    } catch (error) {
      console.error('Error fetching Swahili labels:', error);
      throw error;
    }
  },

  submitTrainingData: async (data) => {
    const response = await axios.post(`${API_BASE_URL}/admin/training-data`, data);
    return response.data;
  },

  // Add training data
  addTrainingData: async (data) => {
    try {
      const response = await api.post('/training/add', {
        text: data.text,
        is_spam: data.is_spam
      });
      return response.data;
    } catch (error) {
      console.error('Error submitting training data:', error);
      throw error;
    }
  },

  // Get system metrics
  getMetrics: async () => {
    try {
      const response = await api.get('/metrics');
      return response.data;
    } catch (error) {
      console.error('Error fetching metrics:', error);
      throw error;
    }
  },

  // Get detailed system stats
  getSystemStats: async () => {
    try {
      const response = await api.get('/stats');
      return response.data;
    } catch (error) {
      console.error('Error fetching system stats:', error);
      throw error;
    }
  },

  // Get detailed health status
  getDetailedHealth: async () => {
    try {
      const response = await api.get('/health/detailed');
      return response.data;
    } catch (error) {
      console.error('Error fetching detailed health:', error);
      throw error;
    }
  }
};

export default api; 