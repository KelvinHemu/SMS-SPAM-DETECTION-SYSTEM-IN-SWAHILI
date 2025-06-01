#!/usr/bin/env python3
"""
Test Script for Two-Party Messaging System
Demonstrates sender → system → receiver message flow
"""

import asyncio
import json
from datetime import datetime
from api.models import MessageAnalysisRequest, DecisionOutcome
from services.message_analysis import MessageAnalysisService
from core.logging import setup_logging, get_logger

# Setup logging
setup_logging()
logger = get_logger()


async def test_two_party_messaging():
    """Test the complete two-party messaging flow"""
    
    print("=" * 80)
    print("🔥 SPAM DETECTION: TWO-PARTY MESSAGING SYSTEM TEST")
    print("=" * 80)
    print()
    
    # Initialize the service
    print("📡 Initializing message analysis service...")
    service = MessageAnalysisService()
    print("✅ Service initialized with delivery capability")
    print()
    
    # Test scenarios
    test_scenarios = [
        {
            "name": "Clean Message",
            "text": "Habari za mchana, je hali gani? Tutaonana kesho",
            "sender": "+255712345678", 
            "receiver": "+255787654321",
            "expected": "CLEAN"
        },
        {
            "name": "Suspicious Content", 
            "text": "Umeshinda milioni 50, piga simu kwa maelezo zaidi",
            "sender": "+255712345678",
            "receiver": "+255787654321", 
            "expected": "CONTENT_WARNING or SENDER_WARNING"
        },
        {
            "name": "Flagged Sender + Spam Content",
            "text": "WIN BIG NOW!!! Call +123456789 immediately for your prize money!!!",
            "sender": "+255787123456",  # This is flagged in mock database
            "receiver": "+255787654321",
            "expected": "BLOCKED"
        },
        {
            "name": "Mixed Language Spam",
            "text": "FREE MONEY! Pata fedha haraka kabisa, piga simu sasa!",
            "sender": "+255765432109",
            "receiver": "+255787654321",
            "expected": "BLOCKED or CONTENT_WARNING"
        },
        {
            "name": "Traditional Healer Spam", 
            "text": "Mganga mkuu, tatua matatizo yako haraka. Piga 0700123456",
            "sender": "+255712345678",
            "receiver": "+255787654321",
            "expected": "CONTENT_WARNING"
        }
    ]
    
    # Run tests
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"📱 TEST {i}: {scenario['name']}")
        print("-" * 60)
        
        # Create request
        request = MessageAnalysisRequest(
            text=scenario["text"],
            sender_phone=scenario["sender"],
            receiver_phone=scenario["receiver"]
        )
        
        print(f"👤 SENDER: {scenario['sender']}")
        print(f"👤 RECEIVER: {scenario['receiver']}")
        print(f"💬 MESSAGE: {scenario['text']}")
        print()
        
        try:
            # Analyze and attempt delivery
            start_time = datetime.now()
            result = await service.analyze_message(request)
            end_time = datetime.now()
            
            processing_time = (end_time - start_time).total_seconds() * 1000
            
            # Display results
            print(f"🎯 DECISION: {result.decision.value}")
            print(f"📊 CONFIDENCE: {result.confidence:.1%}")
            print(f"🏷️  TEXT CLASSIFICATION: {result.text_classification} ({result.text_confidence:.1%})")
            print(f"📞 SENDER STATUS: {result.phone_status} (risk: {result.phone_risk_score:.1%})")
            print(f"⏱️  PROCESSING TIME: {processing_time:.1f}ms")
            print()
            
            # Show delivery outcome
            if result.delivery_result:
                delivery = result.delivery_result
                print(f"🚚 DELIVERY ATTEMPT:")
                print(f"   Status: {delivery.status.value.upper()}")
                print(f"   Delivery ID: {delivery.delivery_id}")
                
                if delivery.status.value == "delivered":
                    print(f"   ✅ DELIVERED TO: {result.receiver_phone}")
                    print(f"   📨 FINAL MESSAGE:")
                    print(f"   {result.labeled_message}")
                elif delivery.status.value == "blocked":
                    print(f"   🚫 BLOCKED - Message not delivered")
                    print(f"   Reason: {delivery.error_message}")
                else:
                    print(f"   ❌ DELIVERY FAILED")
                    print(f"   Error: {delivery.error_message}")
            else:
                print("⚠️  No delivery result available")
            
            print()
            print(f"💭 REASONING: {result.reasoning}")
            print()
            
            # Show expected vs actual
            if scenario["expected"].upper() in result.decision.value.upper():
                print("✅ Result matches expected outcome")
            else:
                print(f"⚠️  Expected: {scenario['expected']}, Got: {result.decision.value}")
            
        except Exception as e:
            print(f"❌ ERROR: {str(e)}")
            logger.error(f"Test scenario failed: {str(e)}")
        
        print("=" * 60)
        print()
    
    # Show delivery statistics
    print("📊 DELIVERY STATISTICS")
    print("-" * 40)
    delivery_stats = service.delivery_service.get_delivery_stats()
    
    print(f"Total Delivery Attempts: {delivery_stats['total_deliveries']}")
    print(f"Successful Deliveries: {delivery_stats['successful_deliveries']}")
    print(f"Blocked Messages: {delivery_stats['blocked_messages']}")
    print(f"Failed Deliveries: {delivery_stats['failed_deliveries']}")
    print(f"Success Rate: {delivery_stats['success_rate']:.1f}%")
    print()
    
    # Show system statistics
    print("🖥️  SYSTEM STATISTICS")
    print("-" * 40)
    system_stats = service.get_system_stats()
    
    print("Decision Breakdown:")
    for decision, count in system_stats['decisions_by_outcome'].items():
        print(f"  {decision}: {count}")
    
    print(f"\nTotal Requests Processed: {system_stats['total_requests']}")
    print(f"Uptime: {system_stats['uptime_seconds']:.1f} seconds")
    print()
    
    print("🎉 Two-party messaging system test completed!")
    print()
    
    # Show flow diagram
    print("📋 TWO-PARTY MESSAGE FLOW SUMMARY")
    print("-" * 50)
    print("1. 👤 Sender sends message to 👤 Receiver")
    print("2. 🔍 System analyzes sender's phone + message content")
    print("3. 🎯 Decision engine determines outcome:")
    print("   • CLEAN → Deliver as-is")
    print("   • CONTENT_WARNING → Deliver with ⚠️ label")
    print("   • SENDER_WARNING → Deliver with ⚠️ label") 
    print("   • BLOCKED → Block delivery completely")
    print("4. 📱 Message delivered to receiver (if not blocked)")
    print("5. 📊 Statistics tracked for monitoring")


async def test_receiver_availability():
    """Test receiver availability checking"""
    print("\n🔍 TESTING RECEIVER AVAILABILITY")
    print("-" * 40)
    
    service = MessageAnalysisService()
    test_receivers = [
        "+255787654321",
        "+255712345678", 
        "+1234567890",
        "invalid-number"
    ]
    
    for receiver in test_receivers:
        try:
            available = await service.delivery_service.check_receiver_availability(receiver)
            status = "✅ Available" if available else "❌ Unavailable"
            print(f"{receiver}: {status}")
        except Exception as e:
            print(f"{receiver}: ❌ Error - {str(e)}")


if __name__ == "__main__":
    # Run the comprehensive test
    asyncio.run(test_two_party_messaging())
    
    # Test receiver availability
    asyncio.run(test_receiver_availability()) 