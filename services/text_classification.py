"""
Text Classification Service
Handles spam/ham classification using the trained ML model
"""

import time
from typing import Tuple
from core.ml_loader import MLModelManager
from core.logging import get_logger
from api.models import TextAnalysisResult, ClassificationResult

logger = get_logger()


class TextClassificationService:
    """Service for text classification using ML model"""
    
    def __init__(self):
        """Initialize the text classification service"""
        self.ml_manager = MLModelManager()
        # Load models if not already loaded
        if not self.ml_manager.is_loaded():
            self.ml_manager.load_models()
        logger.info("Text Classification Service initialized")
    
    def classify_text(self, text: str) -> TextAnalysisResult:
        """
        Classify text as spam or ham using the ML model
        
        Args:
            text: Text to classify
            
        Returns:
            TextAnalysisResult with classification and confidence
        """
        start_time = time.time()
        
        try:
            # Get prediction from ML model
            prediction, confidence = self.ml_manager.predict_text(text)
            
            # Convert to our enum
            classification = ClassificationResult.SPAM if prediction == 'spam' else ClassificationResult.HAM
            
            processing_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            
            result = TextAnalysisResult(
                classification=classification,
                confidence=confidence,
                processing_time_ms=processing_time,
                model_version="v1.0"
            )
            
            logger.info(f"Text classified as {classification.value} with {confidence:.3f} confidence")
            return result
            
        except Exception as e:
            logger.error(f"Error in text classification: {str(e)}")
            # Return conservative result on error
            processing_time = (time.time() - start_time) * 1000
            return TextAnalysisResult(
                classification=ClassificationResult.SPAM,  # Conservative: assume spam on error
                confidence=0.5,
                processing_time_ms=processing_time,
                model_version="v1.0"
            )
    
    def is_model_loaded(self) -> bool:
        """Check if ML model is properly loaded"""
        return self.ml_manager.is_loaded()
    
    def get_model_info(self) -> dict:
        """Get information about the loaded model"""
        try:
            if self.ml_manager.is_loaded():
                vectorizer = self.ml_manager.get_vectorizer()
                return {
                    "model_type": "MultinomialNB",
                    "vectorizer_type": "TfidfVectorizer", 
                    "loaded": True,
                    "vocabulary_size": len(vectorizer.vocabulary_)
                }
            else:
                return {
                    "model_type": "Unknown",
                    "vectorizer_type": "Unknown",
                    "loaded": False,
                    "vocabulary_size": 0
                }
        except Exception as e:
            logger.error(f"Error getting model info: {str(e)}")
            return {
                "model_type": "Error",
                "vectorizer_type": "Error",
                "loaded": False,
                "vocabulary_size": 0
            } 