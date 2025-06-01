import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { ArrowLeft, MessageSquarePlus } from 'lucide-react';
import FeedbackModal from '../components/FeedbackModal';

const FeedbackPage = () => {
  const [isModalOpen, setIsModalOpen] = useState(false);

  return (
    <div className="min-h-screen bg-gray-100 py-12">
      <div className="container mx-auto px-4">
        {/* Header */}
        <div className="mb-8">
          <Link
            to="/"
            className="inline-flex items-center text-blue-600 hover:text-blue-700 mb-4"
          >
            <ArrowLeft className="w-4 h-4 mr-1" />
            Back to Home
          </Link>
          <h1 className="text-3xl font-bold text-gray-800">
            Contribute Feedback
          </h1>
        </div>

        {/* Main Content */}
        <div className="bg-white rounded-xl shadow-md p-6">
          <div className="max-w-2xl mx-auto text-center">
            <div className="text-5xl mb-6">🤖</div>
            <h2 className="text-2xl font-bold text-gray-800 mb-4">
              Help Improve Our Model
            </h2>
            <p className="text-gray-600 mb-8">
              Your feedback helps us improve our Swahili SMS spam detection system.
              Share examples of messages to make our model smarter and more accurate.
            </p>
            <button
              onClick={() => setIsModalOpen(true)}
              className="inline-flex items-center px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              <MessageSquarePlus className="w-5 h-5 mr-2" />
              Add Training Data
            </button>
          </div>

          {/* Information Cards */}
          <div className="grid md:grid-cols-2 gap-6 mt-12">
            <div className="bg-green-50 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-green-800 mb-3">
                Why Contribute?
              </h3>
              <ul className="space-y-2 text-green-700">
                <li>• Improve model accuracy</li>
                <li>• Help identify new spam patterns</li>
                <li>• Protect other users</li>
                <li>• Support Swahili content analysis</li>
              </ul>
            </div>
            <div className="bg-blue-50 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-blue-800 mb-3">
                Best Practices
              </h3>
              <ul className="space-y-2 text-blue-700">
                <li>• Submit real message examples</li>
                <li>• Include various message types</li>
                <li>• Mark spam messages accurately</li>
                <li>• Provide clear examples</li>
              </ul>
            </div>
          </div>
        </div>

        {/* Feedback Modal */}
        <FeedbackModal
          isOpen={isModalOpen}
          onClose={() => setIsModalOpen(false)}
        />
      </div>
    </div>
  );
};

export default FeedbackPage; 