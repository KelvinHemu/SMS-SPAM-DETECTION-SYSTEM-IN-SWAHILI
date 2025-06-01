import React, { useState, useRef, useEffect } from 'react';
import { Send, Phone, ArrowLeft, MoreVertical, Smile } from 'lucide-react';
import { spamDetectionAPI } from '../services/api';
import ReactDOM from 'react-dom/client';

const SenderDevice = ({ onMessageSent, scenarioSelectorContainerId }) => {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [selectedScenario, setSelectedScenario] = useState("verified1");
  const messagesEndRef = useRef(null);
  const textareaRef = useRef(null);

  // Phone scenarios for testing
  const phoneScenarios = {
    // Verified scenarios
    "verified1": {
      senderPhone: "+255712345678",
      receiverPhone: "+255787654321", 
      label: "✅ Verified Business → Regular User",
      category: "verified"
    },
    "verified2": {
      senderPhone: "+255723456789",
      receiverPhone: "+255745678901",
      label: "✅ Registered User → Verified Contact", 
      category: "verified"
    },
    "verified3": {
      senderPhone: "+255734567890",
      receiverPhone: "+255756789012",
      label: "✅ Government → Trusted Contact",
      category: "verified"
    },
    
    // Flagged scenarios
    "flagged1": {
      senderPhone: "+255789123456",
      receiverPhone: "+255787654321",
      label: "🚨 Reported Spam → Regular User",
      category: "flagged"
    },
    "flagged2": {
      senderPhone: "+255765432198", 
      receiverPhone: "+255712345678",
      label: "🚨 High Frequency Sender → Verified User",
      category: "flagged"
    },
    "flagged3": {
      senderPhone: "+255712345698",
      receiverPhone: "+255734567890", 
      label: "🚨 Blacklisted → Government",
      category: "flagged"
    },
    "flagged4": {
      senderPhone: "+255690123456",
      receiverPhone: "+255723456789",
      label: "🚨 Fraud Reported → Registered User",
      category: "flagged"
    }
  };

  const currentScenario = phoneScenarios[selectedScenario];
  const senderPhone = currentScenario.senderPhone;
  const receiverPhone = currentScenario.receiverPhone;
  const currentContact = { number: receiverPhone };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Effect to render scenario selector in external container if ID provided
  useEffect(() => {
    if (scenarioSelectorContainerId) {
      const container = document.getElementById(scenarioSelectorContainerId);
      if (container) {
        const root = ReactDOM.createRoot(container);
        root.render(
          <div className="w-[280px] bg-blue-50 rounded-xl p-4 shadow-md">
            <label className="block text-sm font-medium text-blue-800 mb-2">
              Select Test Scenario:
            </label>
            <select 
              value={selectedScenario}
              onChange={(e) => setSelectedScenario(e.target.value)}
              className="w-full text-sm px-3 py-2 border border-blue-300 rounded-lg bg-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              <optgroup label="✅ Verified Numbers">
                {Object.entries(phoneScenarios)
                  .filter(([key, scenario]) => scenario.category === 'verified')
                  .map(([key, scenario]) => (
                    <option key={key} value={key}>
                      {scenario.label}
                    </option>
                  ))}
              </optgroup>
              <optgroup label="🚨 Flagged Numbers">
                {Object.entries(phoneScenarios)
                  .filter(([key, scenario]) => scenario.category === 'flagged')
                  .map(([key, scenario]) => (
                    <option key={key} value={key}>
                      {scenario.label}
                    </option>
                  ))}
              </optgroup>
            </select>
            <div className="text-sm text-blue-600 mt-2">
              💡 Same message, different results based on sender reputation!
            </div>
          </div>
        );
      }
    }
  }, [scenarioSelectorContainerId, selectedScenario]);

  const sendMessage = async () => {
    if (!newMessage.trim()) return;

    const messageText = newMessage.trim();
    
    // Add message to sender's view immediately as pending
    const pendingMessage = {
      id: Date.now(),
      text: messageText,
      sender: "user",
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      isDelivered: false,
      isPending: true
    };

    setMessages(prev => [...prev, pendingMessage]);
    setNewMessage('');

    try {
      // Send through spam detection API
      const result = await spamDetectionAPI.analyzeMessage(
        senderPhone,
        receiverPhone,
        messageText
      );

      console.log('📤 Message Analysis Result:', result);

      // Update the pending message with final status
      setMessages(prev => prev.map(msg => 
        msg.id === pendingMessage.id 
          ? {
              ...msg,
              isDelivered: result.delivery_result?.status === 'delivered',
              isPending: false,
              decision: result.decision,
              processingTime: result.processing_time_ms
            }
          : msg
      ));

      // Send to receiver if delivered
      if (result.delivery_result?.status === 'delivered' && onMessageSent) {
        onMessageSent({
          id: pendingMessage.id,
          text: messageText,
          senderPhone,
          receiverPhone,
          timestamp: pendingMessage.timestamp,
          analysisResult: result
        });
      }

    } catch (error) {
      console.error('❌ Error sending message:', error);
      
      // Update message to show delivery failure
      setMessages(prev => prev.map(msg => 
        msg.id === pendingMessage.id 
          ? {
              ...msg,
              isDelivered: false,
              isPending: false,
              deliveryError: true
            }
          : msg
      ));
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="flex items-start gap-8">
      {/* Phone Scenario Selector - LEFT SIDE */}
      {!scenarioSelectorContainerId && (
        <div className="w-[280px] bg-blue-50 rounded-xl p-4 shadow-md">
          <label className="block text-sm font-medium text-blue-800 mb-2">
            Select Test Scenario:
          </label>
          <select 
            value={selectedScenario}
            onChange={(e) => setSelectedScenario(e.target.value)}
            className="w-full text-sm px-3 py-2 border border-blue-300 rounded-lg bg-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          >
            <optgroup label="✅ Verified Numbers">
              {Object.entries(phoneScenarios).filter(([key, scenario]) => scenario.category === 'verified').map(([key, scenario]) => (
                <option key={key} value={key}>
                  {scenario.label}
                </option>
              ))}
            </optgroup>
            <optgroup label="🚨 Flagged Numbers">
              {Object.entries(phoneScenarios).filter(([key, scenario]) => scenario.category === 'flagged').map(([key, scenario]) => (
                <option key={key} value={key}>
                  {scenario.label}
                </option>
              ))}
            </optgroup>
          </select>
          <div className="text-sm text-blue-600 mt-2">
            💡 Same message, different results based on sender reputation!
          </div>
        </div>
      )}

      <div className="w-[360px] h-[780px] bg-gradient-to-b from-gray-900 to-black shadow-2xl rounded-3xl overflow-hidden flex flex-col relative">
        
        {/* Status Bar */}
        <div className="bg-black px-6 py-3 flex justify-between items-center text-sm text-white">
          <div className="flex items-center gap-2">
            <span className="font-semibold">Airtel</span>
            <div className="w-1 h-1 bg-white rounded-full"></div>
            <span className="text-xs opacity-75">5G</span>
          </div>
          <div className="text-xs font-medium">
            {new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
          </div>
          <div className="flex items-center gap-2">
            <div className="flex gap-1">
              <div className="w-1 h-3 bg-white rounded-full"></div>
              <div className="w-1 h-3 bg-white rounded-full"></div>
              <div className="w-1 h-3 bg-white rounded-full"></div>
              <div className="w-1 h-3 bg-white rounded-full"></div>
            </div>
            <div className="w-6 h-3 border border-white rounded-sm relative">
              <div className="w-5 h-full bg-white rounded-sm"></div>
              <div className="absolute -right-1 top-0.5 w-0.5 h-2 bg-white rounded-full"></div>
            </div>
          </div>
        </div>

        {/* Header */}
        <div className="bg-gradient-to-r from-blue-600 to-blue-700 px-4 py-4 flex items-center justify-between shadow-lg">
          <div className="flex items-center gap-3">
            <div className="p-1 hover:bg-white/10 rounded-full transition-colors cursor-pointer">
              <ArrowLeft className="w-5 h-5 text-white" />
            </div>
            <div className="flex items-center gap-3">
              <div className="relative">
                <div className={`w-10 h-10 rounded-full flex items-center justify-center ${
                  currentScenario.category === 'verified' ? 'bg-green-300' : 
                  currentScenario.category === 'flagged' ? 'bg-red-300' : 'bg-gray-300'
                }`}>
                  <div className="w-6 h-6 bg-gray-400 rounded-full"></div>
                </div>
                {/* Status indicator */}
                <div className={`absolute -bottom-1 -right-1 w-4 h-4 rounded-full border-2 border-white ${
                  currentScenario.category === 'verified' ? 'bg-green-500' : 
                  currentScenario.category === 'flagged' ? 'bg-red-500' : 'bg-gray-500'
                }`}></div>
              </div>
              <div>
                <div className="font-semibold text-white text-sm">{currentContact.number}</div>
                <div className={`text-xs ${
                  currentScenario.category === 'verified' ? 'text-green-300' : 
                  currentScenario.category === 'flagged' ? 'text-red-300' : 'text-gray-300'
                }`}>
                  {currentScenario.category === 'verified' ? '✅ Verified Sender' : 
                   currentScenario.category === 'flagged' ? '🚨 Flagged Number' : '❓ Unknown Status'}
                </div>
              </div>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <div className="p-2 hover:bg-white/10 rounded-full transition-colors cursor-pointer">
              <Phone className="w-5 h-5 text-white" />
            </div>
            <div className="p-2 hover:bg-white/10 rounded-full transition-colors cursor-pointer">
              <MoreVertical className="w-5 h-5 text-white" />
            </div>
          </div>
        </div>

        {/* Messages Container */}
        <div className="flex-1 overflow-y-auto px-4 py-6 space-y-4 bg-gradient-to-b from-gray-50 to-white">
          
          {/* Show "Today" label */}
          {messages.length === 0 && (
            <div className="flex justify-center mb-4">
              <div className="bg-gray-200 px-3 py-1 rounded-full text-xs text-gray-600 font-medium">
                Today - Spam Detection Active
              </div>
            </div>
          )}

          {messages.map((message, index) => (
            <div key={message.id}>
              {/* Date separator for first message */}
              {index === 0 && messages.length > 0 && (
                <div className="flex justify-center mb-4">
                  <div className="bg-gray-200 px-3 py-1 rounded-full text-xs text-gray-600 font-medium">
                    Today
                  </div>
                </div>
              )}
              
              {/* All messages are outgoing (right-aligned) in sender view */}
              <div className="flex justify-end mb-3">
                <div className="max-w-[85%]">
                  {/* Timestamp above message */}
                  <div className="text-xs text-gray-500 mb-1 px-1 text-right">
                    {message.timestamp}
                    {/* Processing time indicator */}
                    {message.processingTime && (
                      <span className="ml-1 opacity-60">
                        ({message.processingTime}ms)
                      </span>
                    )}
                  </div>
                  
                  <div className={`px-4 py-3 rounded-2xl rounded-tr-md shadow-sm transition-all ${
                    message.isPending 
                      ? 'bg-gradient-to-r from-gray-400 to-gray-500 text-white'
                      : message.deliveryError
                      ? 'bg-gradient-to-r from-red-400 to-red-500 text-white'
                      : message.decision === 'BLOCKED'
                      ? 'bg-gradient-to-r from-red-500 to-red-600 text-white'
                      : 'bg-gradient-to-r from-blue-500 to-blue-600 text-white'
                  }`}>
                    
                    <div className="text-sm leading-relaxed">
                      {message.text}
                    </div>
                    
                    <div className="text-xs mt-2 flex items-center gap-2 opacity-75 justify-end">
                      {/* Delivery status */}
                      <div className="flex gap-1">
                        {message.isPending ? (
                          <div className="flex gap-1">
                            <div className="w-1 h-1 bg-yellow-300 rounded-full animate-pulse"></div>
                            <div className="w-1 h-1 bg-yellow-300 rounded-full animate-pulse"></div>
                          </div>
                        ) : message.deliveryError ? (
                          <span className="text-red-200">❌</span>
                        ) : message.decision === 'BLOCKED' ? (
                          <span className="text-red-200">🚫</span>
                        ) : message.isDelivered ? (
                          <div className="flex gap-1">
                            <div className="w-1 h-1 bg-blue-200 rounded-full"></div>
                            <div className="w-1 h-1 bg-blue-200 rounded-full"></div>
                          </div>
                        ) : (
                          <span className="text-gray-300">○</span>
                        )}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ))}
          
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="bg-white border-t border-gray-100 px-4 py-4 shadow-lg">
          <div className="flex items-end gap-3">
            <div className="flex-1 bg-gray-100 rounded-2xl px-4 py-3 border border-gray-200 focus-within:border-blue-300 focus-within:bg-white transition-all">
              <textarea
                ref={textareaRef}
                value={newMessage}
                onChange={(e) => setNewMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Type a message..."
                className="w-full bg-transparent resize-none outline-none text-sm text-gray-800 placeholder-gray-500"
                rows="1"
                style={{ minHeight: '20px', maxHeight: '100px' }}
              />
            </div>
            
            <button className="p-2 text-gray-500 hover:text-blue-500 hover:bg-blue-50 rounded-full transition-colors">
              <Smile className="w-5 h-5" />
            </button>
            
            <button
              onClick={sendMessage}
              className={`p-3 rounded-full transition-all transform hover:scale-105 ${
                newMessage.trim()
                  ? 'bg-gradient-to-r from-blue-500 to-blue-600 text-white shadow-lg hover:shadow-xl'
                  : 'bg-gray-200 text-gray-400 cursor-not-allowed'
              }`}
              disabled={!newMessage.trim()}
            >
              <Send className="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SenderDevice; 