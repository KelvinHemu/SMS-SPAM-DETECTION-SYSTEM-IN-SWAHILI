import React, { useState } from 'react';
import SenderDevice from '../components/SenderDevice';
import ReceiverDevice from '../components/ReceiverDevice';

const HomePage = () => {
  const [receivedMessages, setReceivedMessages] = useState([]);

  const handleMessageSent = (message) => {
    console.log('📱 App: Message sent from sender:', message);
    
    // Add message to receiver's messages
    const newMessage = {
      id: Date.now(),
      text: message.text,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      analysisResult: message.analysisResult
    };
    
    setReceivedMessages(prev => [...prev, newMessage]);
    console.log('📱 App: Message delivered to receiver');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 p-8">
      {/* Main Title */}
      <h1 className="text-4xl font-bold text-center mb-12 text-gray-800">
        Swahili SMS Spam Detection
      </h1>

      {/* Main Content Container */}
      <div className="flex flex-col items-center">
        {/* Devices and Scenario Container */}
        <div className="flex items-start justify-center gap-12">
          {/* Devices Container - Side by Side */}
          <div className="flex items-center gap-16">
            {/* Sender Device */}
            <SenderDevice onMessageSent={handleMessageSent} />

            {/* Receiver Device */}
            <ReceiverDevice receivedMessages={receivedMessages} />
          </div>
        </div>

        {/* How It Works Section */}
        <div className="max-w-4xl mx-auto mt-16 px-4">
          <h2 className="text-2xl font-bold text-center mb-8 text-gray-800">
            How It Works
          </h2>
          
          <div className="grid md:grid-cols-3 gap-8">
            {/* Step 1 */}
            <div className="bg-white rounded-xl p-6 shadow-lg">
              <div className="text-xl font-bold text-blue-600 mb-2">Step 1</div>
              <h3 className="text-lg font-semibold mb-3">Select Scenario</h3>
              <p className="text-gray-600">
                Choose from different test scenarios to see how the system handles various types of messages and senders.
              </p>
            </div>

            {/* Step 2 */}
            <div className="bg-white rounded-xl p-6 shadow-lg">
              <div className="text-xl font-bold text-blue-600 mb-2">Step 2</div>
              <h3 className="text-lg font-semibold mb-3">Send Message</h3>
              <p className="text-gray-600">
                Type and send a message from the sender device. The system will analyze it for potential spam content.
              </p>
            </div>

            {/* Step 3 */}
            <div className="bg-white rounded-xl p-6 shadow-lg">
              <div className="text-xl font-bold text-blue-600 mb-2">Step 3</div>
              <h3 className="text-lg font-semibold mb-3">View Results</h3>
              <p className="text-gray-600">
                See how the message appears on the receiver's device with any applicable spam warnings or labels.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage; 