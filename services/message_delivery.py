"""
Message Delivery Service
Handles sending processed messages to receivers via SMS
"""

import asyncio
from datetime import datetime
from typing import Optional
import uuid

from core.logging import get_logger
from api.models import (
    DecisionOutcome,
    DeliveryStatus, 
    MessageDeliveryResult
)

logger = get_logger()


class MessageDeliveryService:
    """Service for delivering processed messages to receivers"""
    
    def __init__(self):
        """Initialize the delivery service"""
        self.delivery_stats = {
            "total_deliveries": 0,
            "successful_deliveries": 0, 
            "blocked_messages": 0,
            "failed_deliveries": 0
        }
        logger.info("Message delivery service initialized")
    
    async def deliver_message(
        self,
        receiver_phone: str,
        message_text: str,
        decision: DecisionOutcome,
        sender_phone: str,
        original_message: str
    ) -> MessageDeliveryResult:
        """
        Deliver a processed message to the receiver via SMS
        
        Args:
            receiver_phone: Phone number to deliver message to
            message_text: Processed message text (with labels if needed)
            decision: Decision outcome from analysis
            sender_phone: Original sender's phone number
            original_message: Original unprocessed message
            
        Returns:
            MessageDeliveryResult with delivery status and details
        """
        delivery_id = f"del_{uuid.uuid4().hex[:12]}"
        
        try:
            logger.info(f"Attempting delivery {delivery_id} to {receiver_phone}")
            
            # Check if message should be blocked
            if decision == DecisionOutcome.BLOCKED:
                logger.warning(f"Message blocked from delivery: {delivery_id}")
                result = MessageDeliveryResult(
                    delivery_id=delivery_id,
                    status=DeliveryStatus.BLOCKED,
                    delivered_message=None,
                    error_message="Message blocked due to spam detection"
                )
                self.delivery_stats["blocked_messages"] += 1
                self.delivery_stats["total_deliveries"] += 1
                return result
            
            # Simulate SMS delivery
            sms_success = await self._simulate_sms_delivery(
                receiver_phone=receiver_phone,
                message_text=message_text,
                sender_phone=sender_phone
            )
            
            # Determine overall delivery status
            if sms_success:
                logger.info(f"Message delivered successfully via SMS: {delivery_id}")
                result = MessageDeliveryResult(
                    delivery_id=delivery_id,
                    status=DeliveryStatus.DELIVERED,
                    delivered_message=message_text
                )
                self.delivery_stats["successful_deliveries"] += 1
            else:
                logger.error(f"SMS delivery failed: {delivery_id}")
                result = MessageDeliveryResult(
                    delivery_id=delivery_id,
                    status=DeliveryStatus.FAILED,
                    delivered_message=None,
                    error_message="SMS delivery failed"
                )
                self.delivery_stats["failed_deliveries"] += 1
            
            self.delivery_stats["total_deliveries"] += 1
            return result
            
        except Exception as e:
            logger.error(f"Error in message delivery {delivery_id}: {str(e)}")
            result = MessageDeliveryResult(
                delivery_id=delivery_id,
                status=DeliveryStatus.FAILED,
                delivered_message=None,
                error_message=f"Delivery error: {str(e)}"
            )
            self.delivery_stats["failed_deliveries"] += 1
            self.delivery_stats["total_deliveries"] += 1
            return result
    
    async def _simulate_sms_delivery(
        self,
        receiver_phone: str,
        message_text: str,
        sender_phone: str
    ) -> bool:
        """
        Simulate SMS delivery to receiver
        In production, this would integrate with actual SMS gateway
        
        Args:
            receiver_phone: Receiver's phone number
            message_text: Message to deliver
            sender_phone: Original sender's phone
            
        Returns:
            bool: True if delivery successful, False otherwise
        """
        try:
            # No artificial delay - immediate delivery simulation
            
            # Log the simulated delivery
            logger.info(f"📱 SMS delivered immediately: {sender_phone} -> {receiver_phone}")
            logger.debug(f"SMS content: {message_text}")
            
            # In production, replace this with actual SMS gateway call
            # For demo purposes, assume 98% success rate (very high for immediate delivery)
            import random
            return random.random() > 0.02
            
        except Exception as e:
            logger.error(f"SMS delivery error: {str(e)}")
            return False
    
    def get_delivery_stats(self) -> dict:
        """Get delivery statistics"""
        total = self.delivery_stats["total_deliveries"]
        
        return {
            **self.delivery_stats,
            "success_rate": (self.delivery_stats["successful_deliveries"] / total) * 100 if total > 0 else 0
        }
    
    async def check_receiver_availability(self, receiver_phone: str) -> bool:
        """
        Check if receiver is available for message delivery
        In production, this would check with SMS gateway
        
        Args:
            receiver_phone: Phone number to check
            
        Returns:
            bool: True if receiver is available
        """
        try:
            # No artificial delay - immediate availability check
            
            # For demo purposes, assume 95% availability (high availability)
            import random
            is_available = random.random() > 0.05
            
            logger.debug(f"Receiver availability check: {receiver_phone} -> {'Available' if is_available else 'Unavailable'}")
            return is_available
            
        except Exception as e:
            logger.error(f"Error checking receiver availability: {str(e)}")
            return False


# Global message delivery service instance
delivery_service = MessageDeliveryService() 