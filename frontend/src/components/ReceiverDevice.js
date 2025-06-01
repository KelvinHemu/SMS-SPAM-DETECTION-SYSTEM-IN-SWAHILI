import React, { useEffect, useRef } from 'react';
import { Phone, MoreVertical } from 'lucide-react';

const ReceiverDevice = ({ receivedMessages = [] }) => {
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
    console.log('📱 ReceiverDevice: Received new messages:', receivedMessages.length);
  }, [receivedMessages]);

  return (
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
          <div className="relative">
            <div className="w-10 h-10 rounded-full bg-gray-300 flex items-center justify-center">
              <div className="w-6 h-6 bg-gray-400 rounded-full"></div>
            </div>
            <div className="absolute -bottom-1 -right-1 w-4 h-4 rounded-full border-2 border-white bg-green-500"></div>
          </div>
          <div>
            <div className="font-semibold text-white text-sm">Receiver</div>
            <div className="text-xs text-green-200">Online</div>
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
                  {message.analysisResult?.processing_time_ms && (
                    <span className="ml-1 opacity-60">
                      ({message.analysisResult.processing_time_ms}ms)
                    </span>
                  )}
                </div>
                <div className="bg-white px-4 py-3 rounded-2xl rounded-tl-md shadow-sm">
                  <div className="text-sm leading-relaxed text-gray-800">
                    {message.text}
                  </div>
                  {message.analysisResult && (
                    <div className="mt-1 text-xs text-gray-500">
                      {message.analysisResult.decision === 'CLEAN' && '✅ '}
                      {message.analysisResult.decision === 'WARNING' && '⚠️ '}
                      {message.analysisResult.decision}
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        ))}
        
        <div ref={messagesEndRef} />
      </div>
    </div>
  );
};

export default ReceiverDevice; 