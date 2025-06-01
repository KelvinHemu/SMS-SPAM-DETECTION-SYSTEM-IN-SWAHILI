"""
Message Analysis Service
Main orchestrator for spam detection analysis workflow
"""

import time
from typing import Dict, Any
from core.logging import get_logger
from api.models import (
    MessageAnalysisRequest,
    MessageAnalysisResponse, 
    create_message_id
)
from services.text_classification import TextClassificationService
from services.phone_validation import PhoneValidationService
from services.decision_engine import DecisionEngineService
from services.message_delivery import MessageDeliveryService

logger = get_logger()


class MessageAnalysisService:
    """Main service for complete message analysis workflow"""
    
    def __init__(self):
        """Initialize the message analysis service"""
        self.text_service = TextClassificationService()
        self.phone_service = PhoneValidationService()
        self.decision_service = DecisionEngineService()
        self.delivery_service = MessageDeliveryService()
        
        # Statistics tracking
        self.stats = {
            "total_requests": 0,
            "decisions_by_outcome": {
                "CLEAN": 0,
                "CONTENT_WARNING": 0,
                "SENDER_WARNING": 0,
                "BLOCKED": 0
            },
            "start_time": time.time()
        }
        
        logger.info("Message Analysis Service initialized")
    
    async def analyze_message(self, request: MessageAnalysisRequest) -> MessageAnalysisResponse:
        """
        Perform complete message analysis
        
        Args:
            request: Message analysis request
            
        Returns:
            MessageAnalysisResponse with complete analysis results
        """
        start_time = time.time()
        message_id = create_message_id()
        
        # Get sender phone (prefer sender_phone, fallback to phone_number)
        sender_phone = request.sender_phone or request.phone_number
        
        logger.info(f"Starting analysis for message {message_id}")
        logger.debug(f"[{message_id}] Sender: {sender_phone}, Receiver: {request.receiver_phone}")
        
        try:
            # Step 1: Text Classification
            logger.debug(f"[{message_id}] Step 1: Text classification")
            text_analysis = self.text_service.classify_text(request.text)
            
            # Step 2: Phone Validation (focus on sender phone for spam detection)
            logger.debug(f"[{message_id}] Step 2: Phone validation")
            phone_analysis = self.phone_service.validate_phone(sender_phone)
            
            # Step 3: Decision Making
            logger.debug(f"[{message_id}] Step 3: Decision making")
            combined_analysis = self.decision_service.make_decision(text_analysis, phone_analysis)
            
            # Step 4: Message Delivery (if receiver_phone provided)
            delivery_result = None
            if request.receiver_phone:
                logger.debug(f"[{message_id}] Step 4: Message delivery to {request.receiver_phone}")
                try:
                    delivery_result = await self.delivery_service.deliver_message(
                        receiver_phone=request.receiver_phone,
                        message_text=request.text,  # For now, deliver original text
                        decision=combined_analysis.decision,
                        sender_phone=sender_phone,
                        original_message=request.text
                    )
                    logger.debug(f"[{message_id}] Delivery result: {delivery_result.status}")
                except Exception as e:
                    logger.error(f"[{message_id}] Delivery failed: {str(e)}")
                    # Don't fail the whole analysis if delivery fails
            
            # Calculate total processing time
            total_processing_time = (time.time() - start_time) * 1000
            
            # Create response
            response = MessageAnalysisResponse(
                message_id=message_id,
                decision=combined_analysis.decision,
                confidence=combined_analysis.confidence_score,
                text_classification=text_analysis.classification.value,
                text_confidence=text_analysis.confidence,
                phone_status=phone_analysis.status.value,
                phone_risk_score=phone_analysis.risk_score,
                reasoning=combined_analysis.decision_reasoning,
                delivery_result=delivery_result,
                processing_time_ms=total_processing_time
            )
            
            # Update statistics
            self._update_stats(combined_analysis.decision.value)
            
            logger.info(
                f"[{message_id}] Analysis complete: {combined_analysis.decision.value} "
                f"(confidence: {combined_analysis.confidence_score:.3f}, "
                f"time: {total_processing_time:.1f}ms)"
            )
            
            return response
            
        except Exception as e:
            logger.error(f"[{message_id}] Error in message analysis: {str(e)}")
            
            # Return conservative response on error
            total_processing_time = (time.time() - start_time) * 1000
            
            return MessageAnalysisResponse(
                message_id=message_id,
                decision="BLOCKED",  # Conservative approach
                confidence=0.5,
                text_classification="spam",
                text_confidence=0.5,
                phone_status="unknown",
                phone_risk_score=0.5,
                reasoning=f"Analysis error: {str(e)}",
                processing_time_ms=total_processing_time
            )
    
    def _update_stats(self, decision: str):
        """Update internal statistics"""
        self.stats["total_requests"] += 1
        if decision in self.stats["decisions_by_outcome"]:
            self.stats["decisions_by_outcome"][decision] += 1
    
    def get_system_stats(self) -> Dict[str, Any]:
        """
        Get comprehensive system statistics
        
        Returns:
            Dictionary with system statistics
        """
        uptime = time.time() - self.stats["start_time"]
        
        return {
            "total_requests": self.stats["total_requests"],
            "decisions_by_outcome": self.stats["decisions_by_outcome"],
            "phone_database_stats": self.phone_service.get_database_stats(),
            "model_info": self.text_service.get_model_info(),
            "uptime_seconds": uptime,
            "decision_thresholds": self.decision_service.get_current_thresholds()
        }
    
    def health_check(self) -> Dict[str, Any]:
        """
        Perform health check on all components
        
        Returns:
            Health status dictionary
        """
        try:
            return {
                "status": "healthy",
                "models_loaded": self.text_service.is_model_loaded(),
                "database_connected": self.phone_service.is_database_connected(),
                "components": {
                    "text_classification": self.text_service.is_model_loaded(),
                    "phone_validation": self.phone_service.is_database_connected(),
                    "decision_engine": True  # Always available
                },
                "total_requests": self.stats["total_requests"]
            }
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return {
                "status": "unhealthy",
                "error": str(e),
                "models_loaded": False,
                "database_connected": False
            }
    
    def reset_stats(self):
        """Reset statistics (for admin use)"""
        self.stats = {
            "total_requests": 0,
            "decisions_by_outcome": {
                "CLEAN": 0,
                "CONTENT_WARNING": 0,
                "SENDER_WARNING": 0,
                "BLOCKED": 0
            },
            "start_time": time.time()
        }
        logger.info("Statistics reset")
    
    def add_training_data(self, text: str, phone: str, is_spam: bool, is_phone_flagged: bool) -> Dict[str, bool]:
        """
        Add training data for both text and phone systems
        
        Args:
            text: Message text
            phone: Phone number
            is_spam: Whether the message is spam
            is_phone_flagged: Whether the phone should be flagged
            
        Returns:
            Dictionary indicating success for each component
        """
        results = {}
        
        # Add phone record
        phone_risk = 0.8 if is_phone_flagged else 0.1
        phone_reason = "Manually flagged as spam" if is_phone_flagged else "Manually validated"
        
        results["phone_added"] = self.phone_service.add_phone_record(
            phone_number=phone,
            is_validated=not is_phone_flagged,
            risk_score=phone_risk,
            reason=phone_reason
        )
        
        # Note: Text model retraining would require additional infrastructure
        # For now, we just log the training data
        results["text_logged"] = True
        logger.info(f"Training data logged: text_spam={is_spam}, phone_flagged={is_phone_flagged}")
        
        return results 