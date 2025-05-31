"""
ML Model Loading and Management
"""

import joblib
import os
from typing import Tuple, Any, Optional
from loguru import logger
from sklearn.base import BaseEstimator
from sklearn.feature_extraction.text import CountVectorizer

from .config import get_settings


class MLModelManager:
    """Manages loading and caching of ML models"""
    
    def __init__(self):
        self.settings = get_settings()
        self._model: Optional[BaseEstimator] = None
        self._vectorizer: Optional[CountVectorizer] = None
        self._is_loaded = False
        
    def load_models(self) -> bool:
        """Load ML model and vectorizer from disk"""
        try:
            logger.info("Loading ML models...")
            
            # Validate model files exist
            self.settings.validate_model_files()
            
            # Load the trained model
            logger.info(f"Loading model from: {self.settings.model_path}")
            self._model = joblib.load(self.settings.model_path)
            
            # Load the vectorizer
            logger.info(f"Loading vectorizer from: {self.settings.vectorizer_path}")
            self._vectorizer = joblib.load(self.settings.vectorizer_path)
            
            self._is_loaded = True
            logger.success("ML models loaded successfully!")
            
            # Log model info
            logger.info(f"Model type: {type(self._model).__name__}")
            logger.info(f"Model classes: {getattr(self._model, 'classes_', 'Unknown')}")
            logger.info(f"Vectorizer vocabulary size: {len(self._vectorizer.vocabulary_)}")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to load ML models: {e}")
            self._is_loaded = False
            raise
    
    def get_model(self) -> BaseEstimator:
        """Get the loaded ML model"""
        if not self._is_loaded or self._model is None:
            raise RuntimeError("ML model not loaded. Call load_models() first.")
        return self._model
    
    def get_vectorizer(self) -> CountVectorizer:
        """Get the loaded vectorizer"""
        if not self._is_loaded or self._vectorizer is None:
            raise RuntimeError("Vectorizer not loaded. Call load_models() first.")
        return self._vectorizer
    
    def get_models(self) -> Tuple[BaseEstimator, CountVectorizer]:
        """Get both model and vectorizer"""
        return self.get_model(), self.get_vectorizer()
    
    def is_loaded(self) -> bool:
        """Check if models are loaded"""
        return self._is_loaded
    
    def predict_text(self, text: str) -> Tuple[str, float]:
        """
        Predict spam/ham for a single text
        
        Args:
            text: Input text to classify
            
        Returns:
            Tuple of (prediction, confidence)
        """
        if not self._is_loaded:
            raise RuntimeError("Models not loaded")
            
        try:
            # Validate input
            if not text or not text.strip():
                raise ValueError("Text cannot be empty")
                
            # Truncate if too long
            if len(text) > self.settings.max_text_length:
                text = text[:self.settings.max_text_length]
                logger.warning(f"Text truncated to {self.settings.max_text_length} characters")
            
            # Transform text
            text_vector = self._vectorizer.transform([text])
            
            # Get prediction
            prediction = self._model.predict(text_vector)[0]
            
            # Get confidence (probability)
            probabilities = self._model.predict_proba(text_vector)[0]
            confidence = probabilities.max()
            
            logger.debug(f"Text prediction: {prediction} (confidence: {confidence:.3f})")
            
            return prediction, confidence
            
        except Exception as e:
            logger.error(f"Error predicting text: {e}")
            raise


# Global model manager instance
ml_manager = MLModelManager()


def get_ml_manager() -> MLModelManager:
    """Get the global ML model manager instance"""
    return ml_manager


def initialize_models() -> bool:
    """Initialize ML models at startup"""
    try:
        return ml_manager.load_models()
    except Exception as e:
        logger.error(f"Failed to initialize ML models: {e}")
        return False 