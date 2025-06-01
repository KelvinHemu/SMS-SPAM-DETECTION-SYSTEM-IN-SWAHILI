import React, { useEffect, useRef, useState } from 'react';
import { Phone, MoreVertical, Send, Smile } from 'lucide-react';

// Swahili label mappings from message_labeler.py
const SWAHILI_LABELS = {
  'CLEAN': "",  // No label for clean messages
  'CONTENT_WARNING': "⚠️ Tahadhari: Epuka Matapeli",  // Warning: Avoid Fraud/Scams
  'SENDER_WARNING': "⚠️ Tahadhari: Epuka Matapeli",   // Warning: Avoid Fraud/Scams
  'BLOCKED': "🚫 Imezuiliwa: SPAM"  // Blocked: SPAM
};

const ReceiverDevice = ({ receivedMessages = [] }) => {
  const messagesEndRef = useRef(null);
  const textareaRef = useRef(null);
  const [newMessage, setNewMessage] = useState('');

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
    console.log('📱 ReceiverDevice: Received new messages:', receivedMessages.length);
  }, [receivedMessages]);

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const sendMessage = () => {
    if (!newMessage.trim()) return;
    setNewMessage('');
  };

  return (
    <div className="w-[288px] h-[624px] bg-gradient-to-b from-gray-900 to-black shadow-2xl rounded-3xl overflow-hidden flex flex-col relative">
      {/* Status Bar */}
      <div className="bg-black px-6 py-3 flex justify-between items-center text-sm text-white">
        <div className="flex items-center gap-2">
          <span className="font-semibold">Vodacom</span>
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
          <div className="relative">
            <div className="w-10 h-10 rounded-full bg-gray-300 flex items-center justify-center">
              <div className="w-6 h-6 bg-gray-400 rounded-full"></div>
            </div>
          </div>
          <div>
            <div className="font-semibold text-white text-sm">Receiver</div>
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
        {receivedMessages.length === 0 && (
          <div className="flex justify-center mb-4">
            <div className="bg-gray-200 px-3 py-1 rounded-full text-xs text-gray-600 font-medium">
              Today - Waiting for Messages
            </div>
          </div>
        )}

        {receivedMessages.map((message, index) => (
          <div key={message.id}>
            {/* Date separator for first message */}
            {index === 0 && (
              <div className="flex justify-center mb-4">
                <div className="bg-gray-200 px-3 py-1 rounded-full text-xs text-gray-600 font-medium">
                  Today
                </div>
              </div>
            )}
            
            {/* Incoming message */}
            <div className="flex mb-3">
              <div className="max-w-[85%]">
                <div className="text-xs text-gray-500 mb-1 px-1">
                  {message.timestamp}
                </div>
                <div className="bg-white px-4 py-3 rounded-2xl rounded-tl-md shadow-sm">
                  {/* Show Swahili label if message is not clean */}
                  {message.analysisResult && message.analysisResult.decision !== 'CLEAN' && (
                    <div className="mb-2 text-xs font-medium text-red-600">
                      {SWAHILI_LABELS[message.analysisResult.decision]}
                    </div>
                  )}
                  
                  {/* Message text */}
                  <div className="text-sm leading-relaxed text-gray-800">
                    {message.text}
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

export default ReceiverDevice; 