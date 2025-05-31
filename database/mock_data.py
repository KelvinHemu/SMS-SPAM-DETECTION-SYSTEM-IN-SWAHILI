"""
Mock Phone Validation Database
Simulates external phone validation system
"""

from typing import Dict, Optional, Literal
from dataclasses import dataclass
from loguru import logger

PhoneStatus = Literal["validated", "flagged"]


@dataclass
class PhoneRecord:
    """Phone number validation record"""
    phone_number: str
    status: PhoneStatus
    reason: str
    risk_score: float  # 0.0 = safe, 1.0 = high risk
    last_updated: str


class MockPhoneDatabase:
    """Mock phone validation database"""
    
    def __init__(self):
        self._data: Dict[str, PhoneRecord] = {}
        self._initialize_mock_data()
    
    def _initialize_mock_data(self):
        """Initialize with sample phone data"""
        mock_phones = [
            # Validated/Safe numbers
            PhoneRecord("0712345678", "validated", "verified_business", 0.1, "2024-01-01"),
            PhoneRecord("0723456789", "validated", "registered_user", 0.2, "2024-01-02"), 
            PhoneRecord("0734567890", "validated", "government_agency", 0.0, "2024-01-03"),
            PhoneRecord("0745678901", "validated", "verified_contact", 0.1, "2024-01-04"),
            PhoneRecord("0756789012", "validated", "trusted_sender", 0.1, "2024-01-05"),
            
            # Flagged/Suspicious numbers
            PhoneRecord("0789123456", "flagged", "reported_spam", 0.9, "2024-01-10"),
            PhoneRecord("0765432198", "flagged", "high_frequency_sender", 0.7, "2024-01-11"),
            PhoneRecord("0723456780", "flagged", "suspicious_pattern", 0.8, "2024-01-12"),
            PhoneRecord("0712345698", "flagged", "blacklisted", 1.0, "2024-01-13"),
            PhoneRecord("0690123456", "flagged", "fraud_reported", 0.95, "2024-01-14"),
            PhoneRecord("0677841672", "flagged", "spam_campaign", 0.85, "2024-01-15"),
            PhoneRecord("0683146464", "flagged", "mass_sender", 0.75, "2024-01-16"),
            
            # Traditional healer numbers (mixed status)
            PhoneRecord("0683817701", "flagged", "spiritual_services_spam", 0.8, "2024-01-20"),
            PhoneRecord("0629808228", "flagged", "traditional_healer_spam", 0.9, "2024-01-21"),
            PhoneRecord("0788901234", "validated", "legitimate_traditional_healer", 0.3, "2024-01-22"),
            
            # Additional test numbers
            PhoneRecord("0700000001", "flagged", "test_spam", 0.9, "2024-01-25"),
            PhoneRecord("0700000002", "validated", "test_legitimate", 0.1, "2024-01-25"),
        ]
        
        for record in mock_phones:
            self._data[record.phone_number] = record
            
        logger.info(f"Initialized mock phone database with {len(self._data)} records")
    
    def lookup_phone(self, phone_number: str) -> Optional[PhoneRecord]:
        """
        Look up phone number validation status
        
        Args:
            phone_number: Phone number to look up
            
        Returns:
            PhoneRecord if found, None otherwise
        """
        # Normalize phone number (remove spaces, dashes, etc.)
        normalized_phone = self._normalize_phone(phone_number)
        
        record = self._data.get(normalized_phone)
        if record:
            logger.debug(f"Phone lookup: {normalized_phone} -> {record.status}")
        else:
            logger.debug(f"Phone lookup: {normalized_phone} -> not found")
            
        return record
    
    def get_phone_status(self, phone_number: str) -> PhoneStatus:
        """
        Get phone validation status (validated/flagged)
        
        Args:
            phone_number: Phone number to check
            
        Returns:
            Phone status (defaults to "validated" if not found)
        """
        record = self.lookup_phone(phone_number)
        if record:
            return record.status
        
        # Default to validated for unknown numbers
        logger.info(f"Unknown phone number {phone_number}, defaulting to 'validated'")
        return "validated"
    
    def is_phone_flagged(self, phone_number: str) -> bool:
        """Check if phone number is flagged"""
        return self.get_phone_status(phone_number) == "flagged"
    
    def get_risk_score(self, phone_number: str) -> float:
        """Get risk score for phone number (0.0 = safe, 1.0 = high risk)"""
        record = self.lookup_phone(phone_number)
        return record.risk_score if record else 0.2  # Default low risk
    
    def add_phone_record(self, record: PhoneRecord):
        """Add new phone record (for testing/admin use)"""
        self._data[record.phone_number] = record
        logger.info(f"Added phone record: {record.phone_number} -> {record.status}")
    
    def _normalize_phone(self, phone_number: str) -> str:
        """Normalize phone number format"""
        # Remove common separators
        normalized = phone_number.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
        
        # Add leading zero if missing (Tanzanian format)
        if normalized.startswith("255"):
            normalized = "0" + normalized[3:]
        elif len(normalized) == 9 and normalized.isdigit():
            normalized = "0" + normalized
            
        return normalized
    
    def get_all_records(self) -> Dict[str, PhoneRecord]:
        """Get all phone records (for admin/debugging)"""
        return self._data.copy()
    
    def get_stats(self) -> Dict[str, int]:
        """Get database statistics"""
        validated_count = sum(1 for record in self._data.values() if record.status == "validated")
        flagged_count = sum(1 for record in self._data.values() if record.status == "flagged")
        
        return {
            "total": len(self._data),
            "validated": validated_count,
            "flagged": flagged_count
        }


# Global phone database instance
phone_db = MockPhoneDatabase()


def get_phone_database() -> MockPhoneDatabase:
    """Get the global phone database instance"""
    return phone_db 