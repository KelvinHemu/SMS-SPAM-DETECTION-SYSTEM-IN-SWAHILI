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
  // Analyze message with two-party flow
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
  }
};

export default api; 