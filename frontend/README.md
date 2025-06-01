# Spam Detection UI - Frontend

A React-based frontend for the Two-Party Messaging Spam Detection System.

## 🚀 Features

- **SMS Interface**: Realistic mobile SMS app interface
- **Real-time Spam Detection**: Messages analyzed through ML models
- **Two-Party Flow**: Sender → System → Receiver messaging
- **Swahili Warning Labels**: Automatic warning labels in Swahili
- **Live Dashboard**: Real-time statistics and system health
- **Visual Indicators**: Color-coded decision outcomes
- **Quick Test Buttons**: Pre-loaded test messages for different scenarios

## 📱 Interface Components

### SMS App
- **Phone Number Management**: Switch between sender/receiver
- **Message Processing**: Real-time spam analysis
- **Decision Indicators**: Visual feedback for CLEAN, WARNING, BLOCKED
- **Delivery Status**: Shows pending, delivered, failed states
- **Processing Time**: Displays ML analysis time

### Dashboard
- **System Health**: ML model status and performance
- **Delivery Stats**: Success rates and blocked messages
- **Decision Breakdown**: Distribution of spam detection outcomes
- **Performance Metrics**: Processing times and throughput

## 🛠 Installation

### Prerequisites
- Node.js 16+ and npm
- Backend API running on `http://localhost:8000`

### Setup
```bash
# Install dependencies
npm install

# Start development server
npm start
```

## 🔧 Configuration

The frontend is configured to connect to the backend API at:
- **API Base URL**: `http://localhost:8000/api/v1`
- **Proxy**: Configured in package.json

## 📊 API Integration

### Endpoints Used
- `POST /analyze` - Message analysis and delivery
- `GET /analyze/stats/delivery` - System statistics
- `GET /health` - System health check
- `GET /analyze/test` - Test endpoint
- `GET /analyze/labels` - Swahili label examples

### Message Flow
1. User types message in SMS interface
2. Frontend sends to `/analyze` with sender/receiver phones
3. Backend processes through spam detection pipeline
4. Response includes decision, confidence, delivery status
5. UI updates with results and delivery simulation

## 🧪 Testing

### Quick Test Scenarios
Use the built-in test buttons:

1. **🎰 Test Spam**: `"Umeshinda milioni 50, piga simu kwa maelezo zaidi"`
2. **✅ Test Clean**: `"Habari za mchana, je hali gani?"`
3. **⚠️ Test Warning**: `"WIN BIG NOW!!! Call immediately for your prize!!!"`

### Decision Outcomes
- **CLEAN** 🟢: Safe message, delivered as-is
- **CONTENT_WARNING** 🟡: Suspicious content, delivered with warning
- **SENDER_WARNING** 🟡: Suspicious sender, delivered with warning  
- **BLOCKED** 🔴: High confidence spam, delivery blocked

## 🎨 UI Design

### SMS Interface Features
- **Mobile-first Design**: Responsive for mobile screens
- **Real-time Updates**: Live message status indicators
- **Animated Feedback**: Loading states and transitions
- **Color-coded Results**: Green (clean), Yellow (warning), Red (blocked)
- **Processing Indicators**: Spinning clocks during analysis

### Dashboard Features
- **Live Statistics**: Auto-refreshing every 10 seconds
- **Interactive Charts**: Visual decision breakdown
- **System Monitoring**: ML model health and performance
- **Performance Metrics**: Processing times and success rates

## 🔗 Backend Integration

Ensure the backend spam detection system is running:

```bash
# In the main project directory
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 📱 Phone Number Format

Default phone numbers:
- **Sender**: `+255712345678`
- **Receiver**: `+255787654321`

Use the swap button (⇄) to switch sender/receiver roles.

## 🚨 Error Handling

The frontend handles:
- **API Connection Errors**: Graceful fallback with error messages
- **Network Timeouts**: Retry mechanisms
- **Invalid Responses**: Error state indicators
- **Loading States**: Visual feedback during processing

## 📈 Performance

- **Initial Load**: ~500-600ms (includes model loading)
- **Message Analysis**: ~120-140ms average
- **Dashboard Refresh**: ~10 second intervals
- **API Response Time**: ~130ms for subsequent requests

## 🎯 Production Deployment

For production deployment:

1. **Build the app**: `npm run build`
2. **Serve static files**: Deploy `build/` folder
3. **Update API URL**: Change in `src/services/api.js`
4. **Enable CORS**: Configure backend for frontend domain

## 📝 Development

### Available Scripts
- `npm start` - Development server
- `npm run build` - Production build
- `npm test` - Run tests
- `npm run eject` - Eject from Create React App

### Project Structure
```
frontend/
├── src/
│   ├── components/
│   │   ├── SMSApp.js          # Main SMS interface
│   │   └── SpamDashboard.js   # Statistics dashboard
│   ├── services/
│   │   └── api.js             # API integration
│   ├── App.js                 # Main app component
│   └── index.js               # App entry point
├── public/
│   └── index.html             # HTML template
└── package.json               # Dependencies
```

## 🔍 Troubleshooting

### Common Issues

1. **API Connection Failed**
   - Ensure backend is running on port 8000
   - Check CORS configuration

2. **Messages Not Sending**
   - Verify API endpoints are accessible
   - Check browser console for errors

3. **Dashboard Not Loading**
   - Confirm `/analyze/stats/delivery` endpoint works
   - Check network tab for failed requests

## 🎉 Demo Ready!

The frontend is now ready to demonstrate the complete two-party messaging system with real-time spam detection! 