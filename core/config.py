"""
Application Configuration Management
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # API Settings
    debug: bool = Field(default=True, description="Debug mode")
    api_host: str = Field(default="0.0.0.0", description="API host")
    api_port: int = Field(default=8000, description="API port")
    api_title: str = Field(default="Spam Detection API", description="API title")
    api_version: str = Field(default="1.0.0", description="API version")
    
    # Database
    database_url: str = Field(
        default="sqlite:///./spam_detection.db",
        description="Database connection URL"
    )
    
    # ML Model Paths
    model_path: str = Field(
        default="models/saved_models/spam_classifier_model.pkl",
        description="Path to trained ML model"
    )
    vectorizer_path: str = Field(
        default="models/saved_models/vectorizer.pkl", 
        description="Path to text vectorizer"
    )
    
    # Logging
    log_level: str = Field(default="INFO", description="Logging level")
    log_file: Optional[str] = Field(default=None, description="Log file path")
    
    # Decision Engine Settings
    spam_confidence_threshold: float = Field(
        default=0.5,
        description="Minimum confidence for spam classification",
        ge=0.0,
        le=1.0
    )
    high_risk_threshold: float = Field(
        default=0.7,
        description="Threshold for high phone risk classification",
        ge=0.0,
        le=1.0
    )
    phone_validation_enabled: bool = Field(
        default=True,
        description="Enable phone number validation"
    )
    
    # Performance Settings
    max_text_length: int = Field(
        default=1000,
        description="Maximum text length for processing"
    )
    request_timeout: int = Field(
        default=30,
        description="Request timeout in seconds"
    )
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        
    def validate_model_files(self) -> bool:
        """Validate that ML model files exist"""
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"ML model file not found: {self.model_path}")
        if not os.path.exists(self.vectorizer_path):
            raise FileNotFoundError(f"Vectorizer file not found: {self.vectorizer_path}")
        return True


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get application settings instance"""
    return settings 