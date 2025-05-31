"""
API Models and Data Structures
Defines request/response schemas and internal data types
"""

from typing import Optional, Literal, Dict, Any
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from enum import Enum
import re


# Enums for decision outcomes
class DecisionOutcome(str, Enum):
    """Final decision outcomes for messages"""
    CLEAN = "CLEAN"
    CONTENT_WARNING = "CONTENT_WARNING" 
    SENDER_WARNING = "SENDER_WARNING"
    BLOCKED = "BLOCKED"


class ClassificationResult(str, Enum):
    """Text classification results"""
    HAM = "ham"
    SPAM = "spam"


class PhoneValidationStatus(str, Enum):
    """Phone validation status"""
    VALIDATED = "validated"
    FLAGGED = "flagged"
    UNKNOWN = "unknown"


# Request Models
class MessageAnalysisRequest(BaseModel):
    """Request model for message analysis"""
    text: str = Field(
        ..., 
        description="Message text to analyze",
        min_length=1,
        max_length=1000
    )
    phone_number: str = Field(
        ...,
        description="Sender's phone number"
    )
    
    @field_validator('text')
    @classmethod
    def validate_text(cls, v):
        if not v.strip():
            raise ValueError('Text cannot be empty or only whitespace')
        return v.strip()
    
    @field_validator('phone_number')
    @classmethod
    def validate_phone(cls, v):
        # Check basic phone format
        if not re.match(r"^[\d\+\-\s\(\)]{7,15}$", v):
            raise ValueError('Invalid phone number format')
        
        # Remove spaces and special chars for digit validation
        cleaned = ''.join(c for c in v if c.isdigit())
        if len(cleaned) < 7 or len(cleaned) > 15:
            raise ValueError('Phone number must contain 7-15 digits')
        return v


# Internal Analysis Models
class TextAnalysisResult(BaseModel):
    """Result of text classification analysis"""
    classification: ClassificationResult
    confidence: float = Field(ge=0.0, le=1.0)
    processing_time_ms: float
    model_version: Optional[str] = None


class PhoneAnalysisResult(BaseModel):
    """Result of phone validation analysis"""
    phone_number: str
    status: PhoneValidationStatus
    risk_score: float = Field(ge=0.0, le=1.0)
    reason: Optional[str] = None
    last_updated: Optional[str] = None


class CombinedAnalysisResult(BaseModel):
    """Combined analysis result from both text and phone validation"""
    text_analysis: TextAnalysisResult
    phone_analysis: PhoneAnalysisResult
    decision: DecisionOutcome
    decision_reasoning: str
    confidence_score: float = Field(ge=0.0, le=1.0)
    processing_time_ms: float


# Response Models
class MessageAnalysisResponse(BaseModel):
    """Response model for message analysis"""
    message_id: str = Field(description="Unique identifier for this analysis")
    decision: DecisionOutcome = Field(description="Final decision for the message")
    confidence: float = Field(
        ge=0.0, 
        le=1.0,
        description="Overall confidence in the decision (0.0-1.0)"
    )
    
    # Analysis details
    text_classification: str = Field(description="Text classification result (ham/spam)")
    text_confidence: float = Field(
        ge=0.0, 
        le=1.0,
        description="Confidence in text classification"
    )
    
    phone_status: str = Field(description="Phone validation status")
    phone_risk_score: float = Field(
        ge=0.0, 
        le=1.0,
        description="Phone number risk score"
    )
    
    # Explanation
    reasoning: str = Field(description="Human-readable explanation of the decision")
    
    # Metadata
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    processing_time_ms: float = Field(description="Total processing time in milliseconds")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class HealthCheckResponse(BaseModel):
    """Health check response"""
    status: str = "healthy"
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    version: str
    models_loaded: bool
    database_connected: bool
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str = Field(description="Error type")
    message: str = Field(description="Error message")
    details: Optional[Dict[str, Any]] = Field(default=None, description="Additional error details")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


# Statistics and Admin Models
class SystemStatsResponse(BaseModel):
    """System statistics response"""
    total_requests: int
    decisions_by_outcome: Dict[str, int]
    phone_database_stats: Dict[str, int]
    model_info: Dict[str, Any]
    uptime_seconds: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


# Decision Matrix Configuration (for admin use)
class DecisionMatrixConfig(BaseModel):
    """Configuration for decision matrix logic"""
    spam_confidence_threshold: float = Field(ge=0.0, le=1.0, default=0.5)
    high_risk_threshold: float = Field(ge=0.0, le=1.0, default=0.7)
    content_warning_threshold: float = Field(ge=0.0, le=1.0, default=0.3)
    
    # Decision rules
    enable_phone_validation: bool = True
    enable_text_classification: bool = True
    strict_mode: bool = False  # If true, be more aggressive in blocking


# Utility Functions
def create_message_id() -> str:
    """Generate unique message ID"""
    import uuid
    return f"msg_{uuid.uuid4().hex[:12]}"


def calculate_combined_confidence(
    text_confidence: float,
    phone_risk_score: float,
    decision: DecisionOutcome
) -> float:
    """
    Calculate overall confidence based on text analysis and phone validation
    
    Args:
        text_confidence: Confidence from text classification
        phone_risk_score: Risk score from phone validation
        decision: Final decision outcome
        
    Returns:
        Combined confidence score (0.0-1.0)
    """
    if decision == DecisionOutcome.BLOCKED:
        # High confidence in blocking decisions
        return min(0.95, max(text_confidence, 1 - phone_risk_score))
    elif decision == DecisionOutcome.CLEAN:
        # Confidence in clean messages
        return min(0.9, text_confidence * (1 - phone_risk_score))
    else:
        # Medium confidence for warnings
        return 0.6 + (text_confidence * 0.3) 