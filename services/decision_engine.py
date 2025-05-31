"""
Decision Engine Service
Implements the decision matrix logic for determining final message disposition
"""

from core.config import get_settings
from core.logging import get_logger
from api.models import (
    DecisionOutcome, 
    TextAnalysisResult, 
    PhoneAnalysisResult,
    CombinedAnalysisResult,
    ClassificationResult,
    PhoneValidationStatus,
    calculate_combined_confidence
)

logger = get_logger()


class DecisionEngineService:
    """Service for making final decisions based on text and phone analysis"""
    
    def __init__(self):
        """Initialize the decision engine service"""
        self.settings = get_settings()
        logger.info("Decision Engine Service initialized")
    
    def make_decision(
        self, 
        text_analysis: TextAnalysisResult, 
        phone_analysis: PhoneAnalysisResult
    ) -> CombinedAnalysisResult:
        """
        Make final decision based on text classification and phone validation
        
        Args:
            text_analysis: Result from text classification
            phone_analysis: Result from phone validation
            
        Returns:
            CombinedAnalysisResult with final decision and reasoning
        """
        
        # Extract key metrics
        is_spam = text_analysis.classification == ClassificationResult.SPAM
        spam_confidence = text_analysis.confidence if is_spam else (1.0 - text_analysis.confidence)
        phone_risk = phone_analysis.risk_score
        phone_status = phone_analysis.status
        
        # Decision matrix logic based on architecture diagram
        decision, reasoning = self._apply_decision_matrix(
            is_spam=is_spam,
            spam_confidence=spam_confidence,
            phone_risk=phone_risk,
            phone_status=phone_status
        )
        
        # Calculate combined confidence
        combined_confidence = calculate_combined_confidence(
            text_confidence=text_analysis.confidence,
            phone_risk_score=phone_analysis.risk_score,
            decision=decision
        )
        
        # Calculate total processing time
        total_processing_time = text_analysis.processing_time_ms + 5.0  # Add phone lookup overhead
        
        result = CombinedAnalysisResult(
            text_analysis=text_analysis,
            phone_analysis=phone_analysis,
            decision=decision,
            decision_reasoning=reasoning,
            confidence_score=combined_confidence,
            processing_time_ms=total_processing_time
        )
        
        logger.info(f"Decision: {decision.value} (confidence: {combined_confidence:.3f}) - {reasoning}")
        return result
    
    def _apply_decision_matrix(
        self, 
        is_spam: bool, 
        spam_confidence: float, 
        phone_risk: float, 
        phone_status: PhoneValidationStatus
    ) -> tuple[DecisionOutcome, str]:
        """
        Apply the decision matrix logic
        
        Decision Matrix:
        - BLOCKED: High spam confidence + High phone risk OR Flagged phone + Moderate spam
        - SENDER_WARNING: Flagged phone + Low spam OR High phone risk + Low spam  
        - CONTENT_WARNING: Moderate spam + Unknown/Validated phone
        - CLEAN: Low spam + Validated phone OR Low spam + Low phone risk
        
        Args:
            is_spam: Whether text is classified as spam
            spam_confidence: Confidence in spam classification
            phone_risk: Phone risk score (0.0-1.0)
            phone_status: Phone validation status
            
        Returns:
            Tuple of (decision, reasoning)
        """
        
        # Define thresholds from configuration
        high_spam_threshold = self.settings.spam_confidence_threshold  # 0.5
        high_risk_threshold = self.settings.high_risk_threshold  # 0.7
        
        # Adjust thresholds based on strict mode
        if hasattr(self.settings, 'strict_mode') and self.settings.strict_mode:
            high_spam_threshold = max(0.3, high_spam_threshold - 0.2)
            high_risk_threshold = max(0.5, high_risk_threshold - 0.2)
        
        # Categorize levels
        high_spam = is_spam and spam_confidence >= high_spam_threshold
        moderate_spam = is_spam and spam_confidence >= 0.3
        high_phone_risk = phone_risk >= high_risk_threshold
        moderate_phone_risk = phone_risk >= 0.4
        
        # Apply decision matrix
        if phone_status == PhoneValidationStatus.FLAGGED:
            if high_spam or moderate_spam:
                return DecisionOutcome.BLOCKED, f"Flagged phone ({phone_risk:.2f}) + spam content ({spam_confidence:.2f})"
            else:
                return DecisionOutcome.SENDER_WARNING, f"Flagged phone ({phone_risk:.2f}) with non-spam content"
        
        elif high_spam and high_phone_risk:
            return DecisionOutcome.BLOCKED, f"High spam confidence ({spam_confidence:.2f}) + high phone risk ({phone_risk:.2f})"
        
        elif high_spam and moderate_phone_risk:
            return DecisionOutcome.SENDER_WARNING, f"High spam confidence ({spam_confidence:.2f}) + moderate phone risk ({phone_risk:.2f})"
        
        elif moderate_spam and phone_status == PhoneValidationStatus.UNKNOWN:
            return DecisionOutcome.CONTENT_WARNING, f"Moderate spam confidence ({spam_confidence:.2f}) + unknown phone"
        
        elif moderate_spam and phone_status == PhoneValidationStatus.VALIDATED:
            return DecisionOutcome.CONTENT_WARNING, f"Moderate spam confidence ({spam_confidence:.2f}) + validated phone"
        
        elif high_phone_risk and not high_spam:
            return DecisionOutcome.SENDER_WARNING, f"High phone risk ({phone_risk:.2f}) + low spam confidence"
        
        elif phone_status == PhoneValidationStatus.VALIDATED and not moderate_spam:
            return DecisionOutcome.CLEAN, f"Validated phone + non-spam content ({spam_confidence:.2f})"
        
        elif not moderate_spam and phone_risk < 0.3:
            return DecisionOutcome.CLEAN, f"Low spam confidence + low phone risk ({phone_risk:.2f})"
        
        else:
            # Default case - moderate risk
            return DecisionOutcome.CONTENT_WARNING, f"Moderate risk: spam={spam_confidence:.2f}, phone_risk={phone_risk:.2f}"
    
    def update_thresholds(self, spam_threshold: float = None, risk_threshold: float = None) -> bool:
        """
        Update decision thresholds (for admin use)
        
        Args:
            spam_threshold: New spam confidence threshold
            risk_threshold: New phone risk threshold
            
        Returns:
            True if successful
        """
        try:
            if spam_threshold is not None:
                if 0.0 <= spam_threshold <= 1.0:
                    self.settings.spam_confidence_threshold = spam_threshold
                    logger.info(f"Updated spam threshold to {spam_threshold}")
                else:
                    logger.warning(f"Invalid spam threshold: {spam_threshold}")
                    return False
            
            if risk_threshold is not None:
                if 0.0 <= risk_threshold <= 1.0:
                    self.settings.high_risk_threshold = risk_threshold
                    logger.info(f"Updated risk threshold to {risk_threshold}")
                else:
                    logger.warning(f"Invalid risk threshold: {risk_threshold}")
                    return False
            
            return True
        except Exception as e:
            logger.error(f"Error updating thresholds: {str(e)}")
            return False
    
    def get_current_thresholds(self) -> dict:
        """Get current decision thresholds"""
        return {
            "spam_confidence_threshold": self.settings.spam_confidence_threshold,
            "high_risk_threshold": self.settings.high_risk_threshold,
            "strict_mode": getattr(self.settings, 'strict_mode', False)
        } 