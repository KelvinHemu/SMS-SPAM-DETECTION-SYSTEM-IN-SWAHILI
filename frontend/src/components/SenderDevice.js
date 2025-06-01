import React, { useState, useRef, useEffect } from 'react';
import { Send, Phone, ArrowLeft, MoreVertical, Smile } from 'lucide-react';
import { spamDetectionAPI } from '../services/api';

const SenderDevice = ({ onMessageSent }) => {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [senderPhone] = useState("+255712345678");
  const [receiverPhone] = useState("+255787654321");
  const [currentContact] = useState({
    number: receiverPhone
  });
  const messagesEndRef = useRef(null);
  const textareaRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

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
    <div className="w-[360px] h-[780px] mx-auto bg-gradient-to-b from-gray-900 to-black shadow-2xl rounded-3xl overflow-hidden flex flex-col relative">
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
              <div className="w-10 h-10 bg-gray-300 rounded-full flex items-center justify-center">
                <div className="w-6 h-6 bg-gray-400 rounded-full"></div>
              </div>
            </div>
            <div>
              <div className="font-semibold text-white text-sm">{currentContact.number}</div>
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
            
            <div className="flex justify-end mb-2">
              <div className="max-w-xs">
                <div className={`relative px-4 py-3 rounded-2xl shadow-sm rounded-br-md transform hover:scale-105 transition-transform ${
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
                    <span>{message.timestamp}</span>
                    
                    {/* Processing time indicator */}
                    {message.processingTime && (
                      <span className="text-xs opacity-60">
                        ({message.processingTime}ms)
                      </span>
                    )}
                    
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
  );
};

export default SenderDevice; 