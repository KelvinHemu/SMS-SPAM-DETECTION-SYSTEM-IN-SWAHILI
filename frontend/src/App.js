import React, { useState } from 'react';
import SenderDevice from './components/SenderDevice';
import ReceiverDevice from './components/ReceiverDevice';

function App() {
  const [receivedMessages, setReceivedMessages] = useState([]);

  // Handle message sent from sender device
  const handleMessageSent = (messageData) => {
    console.log('📱 App: Message sent from sender:', messageData);
    
    // Only add to receiver if not blocked
    if (messageData.analysisResult.decision !== 'BLOCKED') {
      setReceivedMessages(prev => [...prev, messageData]);
      console.log('📱 App: Message delivered to receiver');
    } else {
      console.log('🚫 App: Message blocked, not delivered to receiver');
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 py-8">
      <div className="max-w-6xl mx-auto px-4">
        <h1 className="text-3xl font-bold text-center text-gray-800 mb-8">
          Spam Detection Demo
        </h1>
        
        <div className="flex justify-center items-start gap-8">
          {/* Sender Device */}
          <div className="text-center">
            <h2 className="text-xl font-semibold text-gray-700 mb-4">Sender</h2>
            <SenderDevice onMessageSent={handleMessageSent} />
          </div>
          
          {/* Receiver Device */}
          <div className="text-center">
            <h2 className="text-xl font-semibold text-gray-700 mb-4">Receiver</h2>
            <ReceiverDevice receivedMessages={receivedMessages} />
          </div>
        </div>
        
        {/* Instructions */}
        <div className="mt-8 max-w-2xl mx-auto bg-white rounded-lg p-6 shadow-md">
          <h3 className="text-lg font-semibold text-gray-800 mb-3">How it works:</h3>
          <ol className="list-decimal list-inside space-y-2 text-gray-600">
            <li>Type a message in the <strong>Sender</strong> device</li>
            <li>Message is analyzed by spam detection API</li>
            <li>If not blocked, message appears in <strong>Receiver</strong> device with spam label</li>
            <li>Try different messages to see different spam detection results</li>
          </ol>
          
          <div className="mt-4 p-4 bg-yellow-50 rounded-lg">
            <h4 className="font-medium text-yellow-800 mb-2">Try these sample messages:</h4>
            <ul className="text-sm text-yellow-700 space-y-1">
              <li>• <strong>"Hello, how are you?"</strong> → Normal delivery (no label)</li>
              <li>• <strong>"FREE MONEY! Click now!"</strong> → ⚠️ Tahadhari: Epuka Matapeli</li>
              <li>• <strong>"Click here to win money: https://bit.ly/scam"</strong> → 🚫 Blocked (won't reach receiver)</li>
              <li>• <strong>"Daktari mkuu anaponya kila ugonjwa"</strong> → 🚫 Blocked (traditional healer spam)</li>
              <li>• <strong>"Congratulations! You won a prize"</strong> → ⚠️ Tahadhari: Epuka Matapeli</li>
            </ul>
            <p className="text-xs text-yellow-600 mt-2">
              ✨ Clean messages appear normal, suspicious messages get Swahili warning labels!
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App; 