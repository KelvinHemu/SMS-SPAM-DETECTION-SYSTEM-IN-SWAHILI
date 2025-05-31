"""
Administration Endpoints
Configuration management and admin operations
"""

from fastapi import APIRouter, HTTPException, Depends, status
from typing import Dict, Any
from pydantic import BaseModel, Field

from core.logging import get_logger
from api.models import ErrorResponse
from services import MessageAnalysisService

logger = get_logger()

# Create router
router = APIRouter()

# Global service instance
analysis_service = None


# Request models for admin operations
class ThresholdUpdateRequest(BaseModel):
    """Request to update decision thresholds"""
    spam_confidence_threshold: float = Field(None, ge=0.0, le=1.0, description="Spam confidence threshold")
    high_risk_threshold: float = Field(None, ge=0.0, le=1.0, description="High phone risk threshold")


class TrainingDataRequest(BaseModel):
    """Request to add training data"""
    text: str = Field(..., min_length=1, max_length=1000, description="Message text")
    phone_number: str = Field(..., description="Phone number")
    is_spam: bool = Field(..., description="Whether the message is spam")
    is_phone_flagged: bool = Field(..., description="Whether the phone should be flagged")


def get_analysis_service() -> MessageAnalysisService:
    """Dependency to get the analysis service instance"""
    global analysis_service
    if analysis_service is None:
        analysis_service = MessageAnalysisService()
        logger.info("Analysis service initialized for admin endpoints")
    return analysis_service


@router.get(
    "/config",
    status_code=status.HTTP_200_OK,
    summary="Get Current Configuration",
    description="""
    Get current system configuration and settings.
    
    **Information Included**:
    - Decision thresholds
    - System parameters
    - Feature flags
    - Performance settings
    """
)
async def get_config(
    service: MessageAnalysisService = Depends(get_analysis_service)
) -> Dict[str, Any]:
    """
    Get current system configuration
    
    Returns:
        Dictionary with current configuration settings
    """
    try:
        thresholds = service.decision_service.get_current_thresholds()
        
        config = {
            "decision_thresholds": thresholds,
            "features": {
                "text_classification": True,
                "phone_validation": True,
                "batch_processing": True,
                "decision_matrix": True
            },
            "limits": {
                "max_text_length": 1000,
                "max_batch_size": 10,
                "request_timeout": 30
            },
            "version": "1.0.0"
        }
        
        logger.info("Configuration retrieved")
        return config
        
    except Exception as e:
        logger.error(f"Error getting configuration: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorResponse(
                error="ConfigError",
                message="Failed to retrieve configuration",
                details={"error": str(e)}
            ).dict()
        )


@router.put(
    "/config/thresholds",
    status_code=status.HTTP_200_OK,
    summary="Update Decision Thresholds",
    description="""
    Update decision threshold configuration.
    
    **Thresholds**:
    - `spam_confidence_threshold`: Minimum confidence for spam classification (0.0-1.0)
    - `high_risk_threshold`: Threshold for high phone risk classification (0.0-1.0)
    
    **Effects**:
    - Lower spam threshold = more aggressive spam detection
    - Lower risk threshold = more phone numbers flagged as risky
    """
)
async def update_thresholds(
    request: ThresholdUpdateRequest,
    service: MessageAnalysisService = Depends(get_analysis_service)
):
    """
    Update decision thresholds
    
    Args:
        request: Threshold update request
        
    Returns:
        Updated configuration
    """
    try:
        # Update thresholds
        success = service.decision_service.update_thresholds(
            spam_threshold=request.spam_confidence_threshold,
            risk_threshold=request.high_risk_threshold
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorResponse(
                    error="ThresholdUpdateError",
                    message="Failed to update thresholds - invalid values",
                    details={"request": request.dict()}
                ).dict()
            )
        
        # Get updated configuration
        updated_thresholds = service.decision_service.get_current_thresholds()
        
        logger.info(f"Thresholds updated: {updated_thresholds}")
        
        return {
            "message": "Thresholds updated successfully",
            "updated_thresholds": updated_thresholds
        }
        
    except HTTPException:
        raise
    
    except Exception as e:
        logger.error(f"Error updating thresholds: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorResponse(
                error="ThresholdUpdateError",
                message="Failed to update thresholds",
                details={"error": str(e)}
            ).dict()
        )


@router.post(
    "/training-data",
    status_code=status.HTTP_201_CREATED,
    summary="Add Training Data",
    description="""
    Add new training data for both text classification and phone validation.
    
    **Use Cases**:
    - Improve model accuracy with new examples
    - Add phone numbers to validation database
    - Correct misclassifications
    - Enhance decision quality
    
    **Note**: Text model retraining requires separate process - this logs the data for future training.
    """
)
async def add_training_data(
    request: TrainingDataRequest,
    service: MessageAnalysisService = Depends(get_analysis_service)
):
    """
    Add training data for model improvement
    
    Args:
        request: Training data request
        
    Returns:
        Success status and details
    """
    try:
        result = service.add_training_data(
            text=request.text,
            phone=request.phone_number,
            is_spam=request.is_spam,
            is_phone_flagged=request.is_phone_flagged
        )
        
        logger.info(f"Training data added: text_spam={request.is_spam}, phone_flagged={request.is_phone_flagged}")
        
        return {
            "message": "Training data added successfully",
            "results": result,
            "data": {
                "text_classified_as": "spam" if request.is_spam else "ham",
                "phone_status": "flagged" if request.is_phone_flagged else "validated"
            }
        }
        
    except Exception as e:
        logger.error(f"Error adding training data: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorResponse(
                error="TrainingDataError",
                message="Failed to add training data",
                details={"error": str(e)}
            ).dict()
        )


@router.post(
    "/reset-stats",
    status_code=status.HTTP_200_OK,
    summary="Reset System Statistics",
    description="""
    Reset all system statistics and counters.
    
    **Resets**:
    - Request counters
    - Decision outcome statistics
    - Uptime counter
    - Performance metrics
    
    **Use Cases**:
    - Clean start for monitoring periods
    - Performance testing preparation
    - Maintenance operations
    """
)
async def reset_statistics(
    service: MessageAnalysisService = Depends(get_analysis_service)
):
    """
    Reset system statistics
    
    Returns:
        Confirmation message
    """
    try:
        service.reset_stats()
        
        logger.info("System statistics reset")
        
        return {
            "message": "System statistics reset successfully",
            "timestamp": "reset"
        }
        
    except Exception as e:
        logger.error(f"Error resetting statistics: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorResponse(
                error="StatsResetError",
                message="Failed to reset statistics",
                details={"error": str(e)}
            ).dict()
        )


@router.get(
    "/phone-database",
    status_code=status.HTTP_200_OK,
    summary="Phone Database Information",
    description="""
    Get information about the phone validation database.
    
    **Information Included**:
    - Total records count
    - Validated vs flagged distribution
    - Database health status
    - Recent activity
    """
)
async def get_phone_database_info(
    service: MessageAnalysisService = Depends(get_analysis_service)
):
    """
    Get phone database information
    
    Returns:
        Phone database statistics and status
    """
    try:
        db_stats = service.phone_service.get_database_stats()
        
        return {
            "database_stats": db_stats,
            "health": {
                "connected": service.phone_service.is_database_connected(),
                "status": "operational" if service.phone_service.is_database_connected() else "disconnected"
            },
            "features": {
                "normalization": True,
                "risk_scoring": True,
                "dynamic_updates": True
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting phone database info: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorResponse(
                error="DatabaseInfoError",
                message="Failed to get database information",
                details={"error": str(e)}
            ).dict()
        )


@router.get(
    "/model-info",
    status_code=status.HTTP_200_OK,
    summary="ML Model Information",
    description="""
    Get detailed information about the loaded ML model.
    
    **Information Included**:
    - Model type and version
    - Training statistics
    - Vocabulary size
    - Performance metrics
    - Loading status
    """
)
async def get_model_info(
    service: MessageAnalysisService = Depends(get_analysis_service)
):
    """
    Get ML model information
    
    Returns:
        Detailed model information
    """
    try:
        model_info = service.text_service.get_model_info()
        model_loaded = service.text_service.is_model_loaded()
        
        return {
            "model_info": model_info,
            "status": {
                "loaded": model_loaded,
                "health": "healthy" if model_loaded else "unhealthy"
            },
            "capabilities": {
                "languages": ["en", "sw"],
                "classes": ["ham", "spam"],
                "confidence_scoring": True,
                "real_time_prediction": True
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting model info: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorResponse(
                error="ModelInfoError",
                message="Failed to get model information",
                details={"error": str(e)}
            ).dict()
        ) 