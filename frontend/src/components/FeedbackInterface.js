import React, { useState } from 'react';
import { spamDetectionAPI } from '../services/api';
import { AlertTriangle, CheckCircle, XCircle, Phone, RefreshCw } from 'lucide-react';

const FeedbackInterface = () => {
  const [formData, setFormData] = useState({
    text: '',
    phone_number: '',
    is_spam: false,
    is_phone_flagged: false
  });
  const [submitStatus, setSubmitStatus] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setSubmitStatus(null);

    try {
      const response = await spamDetectionAPI.submitTrainingData(formData);
      setSubmitStatus({ type: 'success', message: 'Thank you for your contribution!' });
      setFormData({
        text: '',
        phone_number: '',
        is_spam: false,
        is_phone_flagged: false
      });
    } catch (error) {
      setSubmitStatus({ 
        type: 'error', 
        message: error.response?.data?.detail || 'Failed to submit feedback. Please try again.' 
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  return (
    <div className="max-w-2xl mx-auto p-6 bg-white rounded-xl shadow-lg">
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-gray-800 mb-2">Improve Spam Detection</h2>
        <p className="text-gray-600">Help us enhance our system by contributing examples and feedback.</p>
      </div>

      {submitStatus && (
        <div className={`mb-6 p-4 rounded-lg flex items-center gap-3 ${
          submitStatus.type === 'success' 
            ? 'bg-green-50 text-green-700 border border-green-200'
            : 'bg-red-50 text-red-700 border border-red-200'
        }`}>
          {submitStatus.type === 'success' ? (
            <CheckCircle className="w-5 h-5" />
          ) : (
            <AlertTriangle className="w-5 h-5" />
          )}
          <p className="text-sm font-medium">{submitStatus.message}</p>
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Message Text */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Message Text
          </label>
          <textarea
            name="text"
            value={formData.text}
            onChange={handleChange}
            required
            className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            rows="4"
            placeholder="Enter the message text..."
          />
        </div>

        {/* Phone Number */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Phone Number
          </label>
          <div className="relative">
            <Phone className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input
              type="text"
              name="phone_number"
              value={formData.phone_number}
              onChange={handleChange}
              required
              className="w-full pl-12 pr-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              placeholder="+255712345678"
            />
          </div>
        </div>

        {/* Checkboxes */}
        <div className="space-y-4">
          <div className="flex items-center gap-3">
            <input
              type="checkbox"
              id="is_spam"
              name="is_spam"
              checked={formData.is_spam}
              onChange={handleChange}
              className="w-4 h-4 text-blue-600 rounded border-gray-300 focus:ring-blue-500"
            />
            <label htmlFor="is_spam" className="text-sm text-gray-700">
              This message is spam
            </label>
          </div>

          <div className="flex items-center gap-3">
            <input
              type="checkbox"
              id="is_phone_flagged"
              name="is_phone_flagged"
              checked={formData.is_phone_flagged}
              onChange={handleChange}
              className="w-4 h-4 text-blue-600 rounded border-gray-300 focus:ring-blue-500"
            />
            <label htmlFor="is_phone_flagged" className="text-sm text-gray-700">
              This phone number should be flagged
            </label>
          </div>
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={isLoading}
          className={`w-full py-3 px-6 rounded-lg text-white font-medium flex items-center justify-center gap-2 transition-all ${
            isLoading
              ? 'bg-gray-400 cursor-not-allowed'
              : 'bg-blue-600 hover:bg-blue-700 hover:shadow-lg'
          }`}
        >
          {isLoading ? (
            <>
              <RefreshCw className="w-5 h-5 animate-spin" />
              Submitting...
            </>
          ) : (
            'Submit Feedback'
          )}
        </button>
      </form>

      <div className="mt-8 p-4 bg-blue-50 rounded-lg">
        <h3 className="text-lg font-semibold text-blue-800 mb-2">How This Helps</h3>
        <ul className="space-y-2 text-sm text-blue-700">
          <li className="flex items-center gap-2">
            <CheckCircle className="w-4 h-4" />
            Improves model accuracy with new examples
          </li>
          <li className="flex items-center gap-2">
            <CheckCircle className="w-4 h-4" />
            Adds phone numbers to validation database
          </li>
          <li className="flex items-center gap-2">
            <CheckCircle className="w-4 h-4" />
            Corrects misclassifications
          </li>
          <li className="flex items-center gap-2">
            <CheckCircle className="w-4 h-4" />
            Enhances decision quality
          </li>
        </ul>
      </div>
    </div>
  );
};

export default FeedbackInterface; 