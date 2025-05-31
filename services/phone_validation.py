"""
Phone Validation Service
Handles phone number validation using the mock database
"""

import re
from typing import Optional
from database.mock_data import MockPhoneDatabase, PhoneRecord
from core.logging import get_logger
from api.models import PhoneAnalysisResult, PhoneValidationStatus

logger = get_logger()


class PhoneValidationService:
    """Service for phone number validation and risk assessment"""
    
    def __init__(self):
        """Initialize the phone validation service"""
        self.phone_db = MockPhoneDatabase()
        logger.info("Phone Validation Service initialized")
    
    def validate_phone(self, phone_number: str) -> PhoneAnalysisResult:
        """
        Validate phone number and assess risk
        
        Args:
            phone_number: Phone number to validate
            
        Returns:
            PhoneAnalysisResult with validation status and risk score
        """
        try:
            # Normalize phone number for lookup
            normalized_phone = self._normalize_phone(phone_number)
            
            # Look up in database
            phone_record = self.phone_db.lookup_phone(normalized_phone)
            
            if phone_record:
                # Phone found in database
                status = PhoneValidationStatus.VALIDATED if phone_record.status == 'validated' else PhoneValidationStatus.FLAGGED
                
                result = PhoneAnalysisResult(
                    phone_number=phone_number,
                    status=status,
                    risk_score=phone_record.risk_score,
                    reason=phone_record.reason,
                    last_updated=phone_record.last_updated
                )
                
                logger.info(f"Phone {normalized_phone} found: {status.value} (risk: {phone_record.risk_score:.2f})")
                
            else:
                # Phone not in database - unknown status
                result = PhoneAnalysisResult(
                    phone_number=phone_number,
                    status=PhoneValidationStatus.UNKNOWN,
                    risk_score=0.3,  # Default moderate risk for unknown numbers
                    reason="Phone number not found in database"
                )
                
                logger.info(f"Phone {normalized_phone} not found in database")
            
            return result
            
        except Exception as e:
            logger.error(f"Error in phone validation: {str(e)}")
            # Return conservative result on error
            return PhoneAnalysisResult(
                phone_number=phone_number,
                status=PhoneValidationStatus.UNKNOWN,
                risk_score=0.5,  # Moderate risk on error
                reason=f"Validation error: {str(e)}"
            )
    
    def _normalize_phone(self, phone_number: str) -> str:
        """
        Normalize phone number to match database format
        
        Args:
            phone_number: Raw phone number
            
        Returns:
            Normalized phone number
        """
        # Remove all non-digit characters except +
        cleaned = re.sub(r'[^\d+]', '', phone_number)
        
        # Remove leading + if present
        if cleaned.startswith('+'):
            cleaned = cleaned[1:]
        
        # Convert different formats to local format (0XXXXXXXXX)
        if cleaned.startswith('255') and len(cleaned) == 12:
            # +255XXXXXXXXX -> 0XXXXXXXXX
            cleaned = '0' + cleaned[3:]
        elif len(cleaned) == 9 and cleaned.startswith('7'):
            # 7XXXXXXXX -> 07XXXXXXXX
            cleaned = '0' + cleaned
        elif len(cleaned) == 10 and cleaned.startswith('07'):
            # Already in correct format
            pass
        
        return cleaned
    
    def add_phone_record(self, phone_number: str, is_validated: bool, risk_score: float, reason: str = None) -> bool:
        """
        Add or update a phone record in the database
        
        Args:
            phone_number: Phone number to add
            is_validated: Whether the phone is validated
            risk_score: Risk score (0.0-1.0)
            reason: Reason for the classification
            
        Returns:
            True if successful, False otherwise
        """
        try:
            normalized_phone = self._normalize_phone(phone_number)
            status = "validated" if is_validated else "flagged"
            
            record = PhoneRecord(
                phone_number=normalized_phone,
                status=status,
                reason=reason or f"Manually {status}",
                risk_score=risk_score,
                last_updated="2024-01-01"  # Could use current date
            )
            
            self.phone_db.add_phone_record(record)
            return True
            
        except Exception as e:
            logger.error(f"Error adding phone record: {str(e)}")
            return False
    
    def get_database_stats(self) -> dict:
        """Get statistics about the phone database"""
        stats = self.phone_db.get_stats()
        return {
            "total_records": stats["total"],
            "validated_records": stats["validated"],
            "flagged_records": stats["flagged"]
        }
    
    def is_database_connected(self) -> bool:
        """Check if database is accessible"""
        try:
            stats = self.phone_db.get_stats()
            return stats['total'] >= 0
        except Exception:
            return False 