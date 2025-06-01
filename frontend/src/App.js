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
        <div className="mt-8 max-w-4xl mx-auto bg-white rounded-lg p-6 shadow-md">
          <h3 className="text-lg font-semibold text-gray-800 mb-3">How it works:</h3>
          <ol className="list-decimal list-inside space-y-2 text-gray-600">
            <li><strong>Select a phone number</strong> from the dropdown in the Sender device</li>
            <li>Type a message and send it through spam detection API</li>
            <li>Watch how the <strong>same message</strong> gets different results based on sender's phone status</li>
            <li>Messages appear in Receiver device with appropriate spam labels</li>
          </ol>
          
          <div className="mt-4 grid md:grid-cols-2 gap-4">
            {/* Sample Messages */}
            <div className="p-4 bg-yellow-50 rounded-lg">
              <h4 className="font-medium text-yellow-800 mb-2">Jaribu ujumbe huu (Try these messages):</h4>
              <ul className="text-sm text-yellow-700 space-y-1">
                <li>• <strong>"Habari yako? Unahitaji nini?"</strong> → Normal delivery</li>
                <li>• <strong>"FEDHA BURE! Bonyeza hapa kupata shilingi milioni moja www.mshikofasta.com !"</strong> → ⚠️ Tahadhari: Epuka Matapeli</li>
                <li>• <strong>"Hongera! Umeshinda bahati nasibu. Bonyeza: https://bit.ly/scam"</strong> → 🚫 Blocked</li>
                <li>• <strong>"Daktari mkuu anaponya kila ugonjwa. Piga simu 0712345678"</strong> → 🚫 Blocked (spam ya madaktari wa jadi)</li>
                <li>• <strong>"Umeshinda zawadi kubwa! Ongea nasi haraka"</strong> → ⚠️ Tahadhari: Epuka Matapeli</li>
              </ul>
            </div>
            
            {/* Phone Number Scenarios */}
            <div className="p-4 bg-blue-50 rounded-lg">
              <h4 className="font-medium text-blue-800 mb-2">Test Different Phone Scenarios:</h4>
              <ul className="text-sm text-blue-700 space-y-1">
                <li>• <strong>✅ Verified Numbers</strong> → Get warnings for moderate spam</li>
                <li>• <strong>🚨 Flagged Numbers</strong> → Higher chance of blocking</li>
                <li>• <strong>Same message, different results!</strong> Try sending "FEDHA BURE!" from verified vs flagged numbers</li>
                <li>• <strong>Clean messages</strong> from flagged numbers may still get warnings</li>
                <li>• <strong>Spam from verified numbers</strong> gets more lenient treatment</li>
              </ul>
            </div>
          </div>
          
          <p className="text-xs text-gray-600 mt-4 text-center">
            ✨ Ujumbe safi unaonekana kawaida, ujumbe wa matapeli unapata tahadhari za Kiswahili!<br/>
            🔍 The same message can have different outcomes based on sender's phone reputation.
          </p>
        </div>
      </div>
    </div>
  );
}

export default App; 