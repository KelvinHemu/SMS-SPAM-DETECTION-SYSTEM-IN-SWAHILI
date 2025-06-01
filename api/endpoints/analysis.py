"""
Message Analysis Endpoints
Core spam detection API endpoints
"""

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from core.logging import get_logger
from api.models import (
    MessageAnalysisRequest, 
    MessageAnalysisResponse, 
    ErrorResponse
)
from services import MessageAnalysisService

logger = get_logger()

# Create router
router = APIRouter()

# Global service instance (singleton pattern)
analysis_service = None


def get_analysis_service() -> MessageAnalysisService:
    """Dependency to get the analysis service instance"""
    global analysis_service
    if analysis_service is None:
        analysis_service = MessageAnalysisService()
        logger.info("Analysis service initialized for API endpoints")
    return analysis_service


@router.post(
    "/analyze", 
    response_model=MessageAnalysisResponse,
    status_code=status.HTTP_200_OK,
    summary="Analyze Message for Spam",
    description="""
    Analyze a text message and phone number combination for spam content.
    
    This endpoint performs:
    1. **Text Classification**: Uses ML model to classify message content
    2. **Phone Validation**: Checks phone number against database
    3. **Decision Making**: Applies decision matrix to determine final outcome
    
    **Processing Time**: Typically < 20ms
    
    **Decision Outcomes**:
    - `CLEAN`: Safe message, allow delivery
    - `CONTENT_WARNING`: Suspicious content, review recommended  
    - `SENDER_WARNING`: Suspicious sender, flag for review
    - `BLOCKED`: High confidence spam, block delivery
    """
)
async def analyze_message(
    request: MessageAnalysisRequest,
    service: MessageAnalysisService = Depends(get_analysis_service)
) -> MessageAnalysisResponse:
    """
    Analyze a message for spam content
    
    Args:
        request: Message analysis request containing text and phone number
        
    Returns:
        MessageAnalysisResponse with analysis results and decision
        
    Raises:
        HTTPException: For validation errors or processing failures
    """
    try:
        # Get sender phone for logging (prefer sender_phone, fallback to phone_number)
        sender_phone = request.sender_phone or request.phone_number
        logger.info(f"Received analysis request for sender: {sender_phone}, receiver: {request.receiver_phone}")
        
        # Perform analysis
        result = await service.analyze_message(request)
        
        logger.info(f"Analysis complete: {result.decision} (confidence: {result.confidence:.3f})")
        return result
        
    except ValidationError as e:
        logger.warning(f"Validation error in analysis request: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=ErrorResponse(
                error="ValidationError",
                message="Invalid request data",
                details={"validation_errors": e.errors()}
            ).dict()
        )
    
    except Exception as e:
        logger.error(f"Error in message analysis: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorResponse(
                error="AnalysisError", 
                message="Failed to analyze message",
                details={"error": str(e)}
            ).dict()
        )


@router.post(
    "/analyze/batch",
    response_model=list[MessageAnalysisResponse],
    status_code=status.HTTP_200_OK,
    summary="Batch Analyze Multiple Messages",
    description="""
    Analyze multiple messages in a single request for efficiency.
    
    **Limits**: 
    - Maximum 10 messages per batch
    - Each message subject to same validation as single analysis
    
    **Use Cases**:
    - Bulk message processing
    - Batch spam filtering
    - Historical data analysis
    """
)
async def analyze_batch(
    requests: list[MessageAnalysisRequest],
    service: MessageAnalysisService = Depends(get_analysis_service)
) -> list[MessageAnalysisResponse]:
    """
    Analyze multiple messages in batch
    
    Args:
        requests: List of message analysis requests (max 10)
        
    Returns:
        List of MessageAnalysisResponse objects
        
    Raises:
        HTTPException: For validation errors or batch size limits
    """
    try:
        # Validate batch size
        if len(requests) > 10:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorResponse(
                    error="BatchSizeError",
                    message="Batch size exceeds maximum limit of 10 messages",
                    details={"received": len(requests), "max_allowed": 10}
                ).dict()
            )
        
        if len(requests) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorResponse(
                    error="EmptyBatchError",
                    message="Batch request cannot be empty",
                    details={}
                ).dict()
            )
        
        logger.info(f"Processing batch analysis for {len(requests)} messages")
        
        # Process each message
        results = []
        for i, request in enumerate(requests):
            try:
                result = service.analyze_message(request)
                results.append(result)
                logger.debug(f"Batch item {i+1}/{len(requests)}: {result.decision}")
            except Exception as e:
                logger.error(f"Error processing batch item {i+1}: {str(e)}")
                # Create error response for this item
                from api.models import create_message_id
                error_response = MessageAnalysisResponse(
                    message_id=create_message_id(),
                    decision="BLOCKED",  # Conservative approach
                    confidence=0.0,
                    text_classification="error",
                    text_confidence=0.0,
                    phone_status="error",
                    phone_risk_score=1.0,
                    reasoning=f"Processing error: {str(e)}",
                    processing_time_ms=0.0
                )
                results.append(error_response)
        
        logger.info(f"Batch analysis complete: {len(results)} results")
        return results
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    
    except Exception as e:
        logger.error(f"Error in batch analysis: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorResponse(
                error="BatchAnalysisError",
                message="Failed to process batch analysis",
                details={"error": str(e)}
            ).dict()
        )


@router.get(
    "/analyze/test",
    response_model=MessageAnalysisResponse,
    status_code=status.HTTP_200_OK,
    summary="Test Analysis Endpoint",
    description="""
    Test endpoint with predefined message for API validation.
    
    **Use Cases**:
    - API health testing
    - Integration testing
    - Performance benchmarking
    """
)
async def test_analysis(
    service: MessageAnalysisService = Depends(get_analysis_service)
) -> MessageAnalysisResponse:
    """
    Test the analysis endpoint with a predefined message
    
    Returns:
        MessageAnalysisResponse for the test message
    """
    try:
        # Create test request
        test_request = MessageAnalysisRequest(
            text="Umeshinda milioni 50, piga simu kwa maelezo zaidi",
            phone_number="+255787123456"
        )
        
        logger.info("Processing test analysis request")
        result = service.analyze_message(test_request)
        
        logger.info(f"Test analysis complete: {result.decision}")
        return result
        
    except Exception as e:
        logger.error(f"Error in test analysis: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorResponse(
                error="TestAnalysisError",
                message="Failed to process test analysis",
                details={"error": str(e)}
            ).dict()
        ) 