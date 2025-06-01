import React, { useState } from 'react';
import { X, Loader2 } from 'lucide-react';
import { spamDetectionAPI } from '../services/api';

const FeedbackModal = ({ isOpen, onClose }) => {
  const [message, setMessage] = useState('');
  const [isSpam, setIsSpam] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitStatus, setSubmitStatus] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!message.trim()) return;

    setIsSubmitting(true);
    setSubmitStatus(null);

    try {
      await spamDetectionAPI.addTrainingData({
        text: message.trim(),
        is_spam: isSpam
      });

      setSubmitStatus('success');
      setMessage('');
      setIsSpam(false);

      // Close modal after success
      setTimeout(() => {
        onClose();
        setSubmitStatus(null);
      }, 2000);

    } catch (error) {
      console.error('Error submitting feedback:', error);
      setSubmitStatus('error');
    } finally {
      setIsSubmitting(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-xl shadow-xl w-full max-w-md transform transition-all">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b">
          <h2 className="text-xl font-semibold text-gray-800">
            Contribute to Model Training
          </h2>
          <button
            onClick={onClose}
            className="p-1 hover:bg-gray-100 rounded-full transition-colors"
          >
            <X className="w-5 h-5 text-gray-500" />
          </button>
        </div>

        {/* Content */}
        <form onSubmit={handleSubmit} className="p-4 space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Message Text
            </label>
            <textarea
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              rows="4"
              placeholder="Enter a Swahili message..."
            />
          </div>

          <div className="flex items-center gap-4">
            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="radio"
                checked={!isSpam}
                onChange={() => setIsSpam(false)}
                className="w-4 h-4 text-blue-600"
              />
              <span className="text-sm text-gray-700">Normal Message</span>
            </label>
            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="radio"
                checked={isSpam}
                onChange={() => setIsSpam(true)}
                className="w-4 h-4 text-red-600"
              />
              <span className="text-sm text-gray-700">Spam Message</span>
            </label>
          </div>

          {/* Status Messages */}
          {submitStatus === 'success' && (
            <div className="text-sm text-green-600 bg-green-50 px-3 py-2 rounded">
              ✨ Thank you for contributing! Your feedback helps improve the model.
            </div>
          )}
          {submitStatus === 'error' && (
            <div className="text-sm text-red-600 bg-red-50 px-3 py-2 rounded">
              ❌ Error submitting feedback. Please try again.
            </div>
          )}

          {/* Submit Button */}
          <div className="flex justify-end">
            <button
              type="submit"
              disabled={isSubmitting || !message.trim()}
              className={`
                px-4 py-2 rounded-lg text-white font-medium
                flex items-center gap-2 transition-all
                ${isSubmitting 
                  ? 'bg-gray-400 cursor-not-allowed'
                  : message.trim()
                    ? 'bg-blue-600 hover:bg-blue-700'
                    : 'bg-gray-400 cursor-not-allowed'
                }
              `}
            >
              {isSubmitting ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  Training...
                </>
              ) : (
                'Submit Feedback'
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default FeedbackModal; 