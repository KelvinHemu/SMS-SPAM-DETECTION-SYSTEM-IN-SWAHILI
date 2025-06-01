import React, { useState, useRef, useEffect } from 'react';
import { Phone, ArrowLeft, MoreVertical, Send, Smile } from 'lucide-react';

const ReceiverDevice = ({ receivedMessages = [] }) => {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [senderPhone] = useState("+255712345678");
  const [currentContact] = useState({
    number: senderPhone
  });
  const messagesEndRef = useRef(null);
  const textareaRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Update messages when new messages are received
  useEffect(() => {
    console.log('📱 ReceiverDevice: Received new messages:', receivedMessages.length);
    
    const formattedMessages = receivedMessages.map(msg => {
      const spamLabel = getSpamLabel(msg.analysisResult);
      
      return {
        id: msg.id,
        text: msg.text,
        sender: "contact",
        timestamp: msg.timestamp,
        decision: msg.analysisResult.decision,
        confidence: msg.analysisResult.confidence,
        spamLabel: spamLabel,
        analysisResult: msg.analysisResult
      };
    });
    
    setMessages(formattedMessages);
  }, [receivedMessages]);

  // Generate spam detection label for display - matches message_labeler.py
  const getSpamLabel = (analysisResult) => {
    const { decision } = analysisResult;
    
    switch (decision) {
      case 'CLEAN':
        // No label for clean messages - deliver as normal SMS
        return null;
      case 'CONTENT_WARNING':
      case 'SENDER_WARNING':
        return {
          type: 'warning',
          text: "⚠️ Tahadhari: Epuka Matapeli",  // Warning: Avoid Fraud/Scams (Swahili)
          color: 'bg-yellow-100 text-yellow-800 border-yellow-200'
        };
      case 'BLOCKED':
        return {
          type: 'blocked',
          text: "🚫 Imezuiliwa: SPAM",  // Blocked: SPAM (Swahili)
          color: 'bg-red-100 text-red-800 border-red-200'
        };
      default:
        return null;
    }
  };

  const sendMessage = async () => {
    if (!newMessage.trim()) return;

    // Add message to receiver's view immediately (like real SMS)
    const sentMessage = {
      id: Date.now(),
      text: newMessage,
      sender: "user",
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      isRead: true,
      isDelivered: true
    };

    setMessages(prev => [...prev, sentMessage]);
    setNewMessage('');
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  // Render spam label component
  const renderSpamLabel = (spamLabel) => {
    if (!spamLabel) return null;

    return (
      <div className={`mb-2 px-3 py-2 rounded-lg border text-xs font-medium ${spamLabel.color}`}>
        {spamLabel.text}
      </div>
    );
  };

  return (
    <div className="w-[360px] h-[780px] mx-auto bg-gradient-to-b from-gray-900 to-black shadow-2xl rounded-3xl overflow-hidden flex flex-col relative">
      {/* Status Bar */}
      <div className="bg-black px-6 py-3 flex justify-between items-center text-sm text-white">
        <div className="flex items-center gap-2">
          <span className="font-semibold">Vodacom</span>
          <div className="w-1 h-1 bg-white rounded-full"></div>
          <span className="text-xs opacity-75">4G</span>
        </div>
        <div className="text-xs font-medium">
          {new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        </div>
        <div className="flex items-center gap-2">
          <div className="flex gap-1">
            <div className="w-1 h-3 bg-white rounded-full"></div>
            <div className="w-1 h-3 bg-white rounded-full"></div>
            <div className="w-1 h-3 bg-white opacity-60 rounded-full"></div>
            <div className="w-1 h-3 bg-white opacity-40 rounded-full"></div>
          </div>
          <div className="w-6 h-3 border border-white rounded-sm relative">
            <div className="w-3 h-full bg-white rounded-sm"></div>
            <div className="absolute -right-1 top-0.5 w-0.5 h-2 bg-white rounded-full"></div>
          </div>
        </div>
      </div>

      {/* Header */}
      <div className="bg-gradient-to-r from-green-600 to-teal-700 px-4 py-4 flex items-center justify-between shadow-lg">
        <div className="flex items-center gap-3">
          <div className="p-1 hover:bg-white/10 rounded-full transition-colors cursor-pointer">
            <ArrowLeft className="w-5 h-5 text-white" />
          </div>
          <div className="flex items-center gap-3">
            <div className="relative">
              <div className="w-10 h-10 bg-gray-300 rounded-full flex items-center justify-center">
                <div className="w-6 h-6 bg-gray-400 rounded-full"></div>
              </div>
            </div>
            <div>
              <div className="font-semibold text-white text-sm">{currentContact.number}</div>
              <div className="text-xs text-green-300">SMS Active</div>
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
              Today - SMS Ready
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
            
            {message.sender === "contact" ? (
              <div className="flex justify-start mb-2">
                <div className="max-w-xs">
                  <div className="relative px-4 py-3 rounded-2xl shadow-sm bg-white border border-gray-100 rounded-bl-md shadow-md">
                    
                    {/* Spam Detection Label */}
                    {renderSpamLabel(message.spamLabel)}
                    
                    <div className="text-sm leading-relaxed text-gray-800">
                      {/* Check if message contains links */}
                      {message.text.includes('https://') ? (
                        <>
                          <div className="text-gray-700">
                            {message.text.split('\n')[0]} {/* First line */}
                          </div>
                          {message.text.includes('https://') && (
                            <div className="mt-2 p-2 bg-blue-50 rounded-lg">
                              <span className="text-blue-600 underline cursor-pointer hover:text-blue-800 transition-colors text-xs">
                                {message.text.match(/https:\/\/[^\s\n]+/)?.[0]}
                              </span>
                            </div>
                          )}
                        </>
                      ) : (
                        message.text
                      )}
                    </div>
                    
                    <div className="text-xs mt-2 flex items-center gap-1 text-gray-500">
                      <span>{message.timestamp}</span>
                    </div>
                  </div>
                </div>
              </div>
            ) : (
              <div className="flex justify-end mb-2">
                <div className="max-w-xs">
                  <div className="relative px-4 py-3 rounded-2xl shadow-sm bg-gradient-to-r from-green-500 to-green-600 text-white rounded-br-md transform hover:scale-105 transition-transform">
                    
                    <div className="text-sm leading-relaxed text-white">
                      {message.text}
                    </div>
                    
                    <div className="text-xs mt-2 flex items-center gap-1 text-green-100 justify-end">
                      <span>{message.timestamp}</span>
                      <div className="flex gap-1">
                        <div className={`w-1 h-1 rounded-full ${message.isRead ? 'bg-green-200' : 'bg-green-300'}`}></div>
                        <div className={`w-1 h-1 rounded-full ${message.isRead ? 'bg-green-200' : 'bg-green-300'}`}></div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        ))}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="bg-white border-t border-gray-100 px-4 py-4 shadow-lg">
        <div className="flex items-end gap-3">
          <div className="flex-1 bg-gray-100 rounded-2xl px-4 py-3 border border-gray-200 focus-within:border-green-300 focus-within:bg-white transition-all">
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
          
          <button className="p-2 text-gray-500 hover:text-green-500 hover:bg-green-50 rounded-full transition-colors">
            <Smile className="w-5 h-5" />
          </button>
          
          <button
            onClick={sendMessage}
            className={`p-3 rounded-full transition-all transform hover:scale-105 ${
              newMessage.trim()
                ? 'bg-gradient-to-r from-green-500 to-teal-600 text-white shadow-lg hover:shadow-xl'
                : 'bg-gray-200 text-gray-400 cursor-not-allowed'
            }`}
            disabled={!newMessage.trim()}
          >
            <Send className="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default ReceiverDevice; 