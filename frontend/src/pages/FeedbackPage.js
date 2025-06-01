import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowLeft } from 'lucide-react';
import FeedbackInterface from '../components/FeedbackInterface';

const FeedbackPage = () => {
  return (
    <div className="min-h-screen bg-gray-100 py-12">
      <div className="container mx-auto px-4">
        {/* Header with Back Button */}
        <div className="mb-8">
          <Link 
            to="/" 
            className="inline-flex items-center text-blue-600 hover:text-blue-700 transition-colors mb-4"
          >
            <ArrowLeft className="w-5 h-5 mr-1" />
            Back to Messages
          </Link>
          <h1 className="text-3xl font-bold text-gray-800">
            System Improvement
          </h1>
          <p className="text-gray-600 mt-2">
            Help improve our spam detection system by providing feedback and examples.
          </p>
        </div>

        {/* Feedback Interface */}
        <FeedbackInterface />
      </div>
    </div>
  );
};

export default FeedbackPage; 