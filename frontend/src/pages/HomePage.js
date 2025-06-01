import React from 'react';
import { Link } from 'react-router-dom';
import { MessageSquarePlus, BarChart2 } from 'lucide-react';
import SenderDevice from '../components/SenderDevice';
import ReceiverDevice from '../components/ReceiverDevice';

const HomePage = () => {
  const [receivedMessages, setReceivedMessages] = React.useState([]);

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
    <div className="min-h-screen bg-gray-100 py-12">
      <div className="container mx-auto px-4">
        {/* Header */}
        <div className="mb-8 text-center">
          <h1 className="text-3xl font-bold text-gray-800">
            Swahili SMS Spam Detection
          </h1>
        </div>

        <div className="flex gap-8">
          {/* Left Sidebar */}
          <div className="w-[280px] space-y-4">
            {/* System Tools */}
            <div className="bg-white p-4 rounded-lg shadow">
              <h2 className="text-lg font-semibold text-gray-800 mb-3">
                System Tools
              </h2>
              <div className="space-y-2">
                <Link
                  to="/dashboard"
                  className="flex items-center px-4 py-2 text-sm bg-green-50 text-green-700 rounded hover:bg-green-100"
                >
                  <BarChart2 className="w-4 h-4 mr-2" />
                  View Dashboard
                </Link>
                <Link
                  to="/feedback"
                  className="flex items-center px-4 py-2 text-sm bg-blue-50 text-blue-700 rounded hover:bg-blue-100"
                >
                  <MessageSquarePlus className="w-4 h-4 mr-2" />
                  Contribute Feedback
                </Link>
              </div>
            </div>

            {/* Phone Scenario Selector - Will be rendered by SenderDevice */}
            <div id="scenario-selector-container"></div>
          </div>

          {/* Main Content */}
          <div className="flex-1">
            <div className="flex justify-center items-start gap-8">
              <SenderDevice 
                onMessageSent={handleMessageSent} 
                scenarioSelectorContainerId="scenario-selector-container"
              />
              <ReceiverDevice receivedMessages={receivedMessages} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage; 