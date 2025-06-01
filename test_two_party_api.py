#!/usr/bin/env python3
"""
Two-Party Messaging API Test
Tests the new sender → receiver message flow via HTTP API
"""

import httpx
import asyncio
import json
import time
from datetime import datetime


async def test_two_party_api():
    """Test the two-party messaging API endpoints"""
    
    print("=" * 80)
    print("🌐 TWO-PARTY MESSAGING API TEST")
    print("=" * 80)
    print()
    
    base_url = "http://localhost:8000/api/v1"
    
    # Test scenarios for API
    test_cases = [
        {
            "name": "Clean Message Delivery",
            "payload": {
                "text": "Habari za mchana, je hali gani? Tutaonana kesho",
                "sender_phone": "+255712345678",
                "receiver_phone": "+255787654321"
            }
        },
        {
            "name": "Spam Content with Flagged Sender",
            "payload": {
                "text": "WIN BIG NOW!!! Call immediately for your prize money!!!",
                "sender_phone": "+255787123456",  # Flagged in database
                "receiver_phone": "+255787654321"
            }
        },
        {
            "name": "Swahili Spam Detection",
            "payload": {
                "text": "Umeshinda milioni 50, piga simu kwa maelezo zaidi",
                "sender_phone": "+255765432108",
                "receiver_phone": "+255712345678"
            }
        }
    ]
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        
        # Test each scenario
        for i, test_case in enumerate(test_cases, 1):
            print(f"📱 API TEST {i}: {test_case['name']}")
            print("-" * 60)
            
            payload = test_case["payload"]
            print(f"👤 SENDER: {payload['sender_phone']}")
            print(f"👤 RECEIVER: {payload['receiver_phone']}")
            print(f"💬 MESSAGE: {payload['text']}")
            print()
            
            try:
                # Send request to analysis endpoint
                start_time = time.time()
                response = await client.post(
                    f"{base_url}/analyze",
                    json=payload,
                    headers={"Content-Type": "application/json"}
                )
                response_time = (time.time() - start_time) * 1000
                
                if response.status_code == 200:
                    result = response.json()
                    
                    print(f"✅ API Response: {response.status_code}")
                    print(f"⏱️  Response Time: {response_time:.1f}ms")
                    print()
                    
                    # Display analysis results
                    print(f"🎯 DECISION: {result['decision']}")
                    print(f"📊 CONFIDENCE: {result['confidence']:.1%}")
                    print(f"🏷️  TEXT CLASSIFICATION: {result['text_classification']} ({result['text_confidence']:.1%})")
                    print(f"📞 SENDER STATUS: {result['phone_status']} (risk: {result['phone_risk_score']:.1%})")
                    print()
                    
                    # Show delivery outcome
                    if result.get('delivery_result'):
                        delivery = result['delivery_result']
                        print(f"🚚 DELIVERY RESULT:")
                        print(f"   Status: {delivery['status'].upper()}")
                        print(f"   Delivery ID: {delivery['delivery_id']}")
                        
                        if delivery['status'] == 'delivered':
                            print(f"   ✅ DELIVERED TO: {result['receiver_phone']}")
                            print(f"   📨 FINAL MESSAGE:")
                            print(f"   {result['labeled_message']}")
                        elif delivery['status'] == 'blocked':
                            print(f"   🚫 BLOCKED - Message not delivered")
                            print(f"   Reason: {delivery.get('error_message', 'Spam detected')}")
                        else:
                            print(f"   ❌ DELIVERY FAILED: {delivery.get('error_message', 'Unknown error')}")
                    
                    print()
                    print(f"💭 REASONING: {result['reasoning']}")
                    
                else:
                    print(f"❌ API Error: {response.status_code}")
                    print(f"Response: {response.text}")
                
            except Exception as e:
                print(f"❌ Connection Error: {str(e)}")
            
            print("=" * 60)
            print()
        
        # Test the delivery statistics endpoint
        print("📊 TESTING DELIVERY STATISTICS ENDPOINT")
        print("-" * 50)
        
        try:
            response = await client.get(f"{base_url}/analyze/stats/delivery")
            
            if response.status_code == 200:
                stats = response.json()
                
                print("✅ Delivery Statistics Retrieved")
                print()
                
                # Display delivery performance
                delivery_perf = stats.get('delivery_performance', {})
                print(f"📈 DELIVERY PERFORMANCE:")
                print(f"   Total Attempts: {delivery_perf.get('total_deliveries', 0)}")
                print(f"   Successful: {delivery_perf.get('successful_deliveries', 0)}")
                print(f"   Blocked: {delivery_perf.get('blocked_messages', 0)}")
                print(f"   Failed: {delivery_perf.get('failed_deliveries', 0)}")
                print(f"   Success Rate: {delivery_perf.get('success_rate', 0):.1f}%")
                print()
                
                # Display decision breakdown
                decisions = stats.get('message_decisions', {})
                print(f"🎯 DECISION BREAKDOWN:")
                for decision, count in decisions.items():
                    print(f"   {decision}: {count}")
                print()
                
                # Display system health
                health = stats.get('system_health', {})
                print(f"🖥️  SYSTEM HEALTH: {health.get('status', 'unknown').upper()}")
                
                # Display flow info
                flow_info = stats.get('two_party_flow_info', {})
                print()
                print(f"📋 FLOW DESCRIPTION:")
                print(f"   {flow_info.get('description', 'N/A')}")
                
            else:
                print(f"❌ Stats Error: {response.status_code}")
                print(f"Response: {response.text}")
                
        except Exception as e:
            print(f"❌ Stats Connection Error: {str(e)}")
        
        print()
        
        # Test the health endpoint
        print("🏥 TESTING HEALTH ENDPOINT")
        print("-" * 30)
        
        try:
            response = await client.get(f"{base_url}/health")
            
            if response.status_code == 200:
                health = response.json()
                print("✅ Health Check Passed")
                print(f"Status: {health.get('status', 'unknown')}")
                print(f"Models Loaded: {health.get('models_loaded', False)}")
                print(f"Database Connected: {health.get('database_connected', False)}")
            else:
                print(f"❌ Health Check Failed: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Health Check Error: {str(e)}")
    
    print()
    print("🎉 Two-party messaging API test completed!")
    print()
    print("📋 SUMMARY:")
    print("• Sender sends message intended for receiver")
    print("• System analyzes sender's reputation + message content")
    print("• Decision determines delivery outcome:")
    print("  - CLEAN: Deliver message as-is")
    print("  - WARNING: Deliver with Swahili warning label")
    print("  - BLOCKED: Block delivery entirely")
    print("• Receiver gets processed message (if not blocked)")
    print("• All events are logged and tracked")


async def test_api_endpoints_overview():
    """Test and show all available API endpoints"""
    
    print("\n" + "=" * 80)
    print("🔗 API ENDPOINTS OVERVIEW")
    print("=" * 80)
    
    base_url = "http://localhost:8000/api/v1"
    
    endpoints = [
        {"method": "POST", "path": "/analyze", "description": "Analyze and deliver message"},
        {"method": "GET", "path": "/analyze/test", "description": "Test endpoint with sample data"},
        {"method": "GET", "path": "/analyze/labels", "description": "Get Swahili label examples"},
        {"method": "GET", "path": "/analyze/stats/delivery", "description": "Get delivery statistics"},
        {"method": "GET", "path": "/health", "description": "System health check"},
        {"method": "GET", "path": "/", "description": "API root information"}
    ]
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        for endpoint in endpoints:
            print(f"{endpoint['method']} {endpoint['path']}")
            print(f"   📄 {endpoint['description']}")
            
            try:
                if endpoint["method"] == "GET":
                    if endpoint["path"] == "/":
                        response = await client.get("http://localhost:8000/")
                    else:
                        response = await client.get(f"{base_url}{endpoint['path']}")
                    
                    if response.status_code == 200:
                        print(f"   ✅ Available (Status: {response.status_code})")
                    else:
                        print(f"   ⚠️  Response: {response.status_code}")
                else:
                    print(f"   📝 Requires POST data")
                
            except Exception as e:
                print(f"   ❌ Error: {str(e)}")
            
            print()


if __name__ == "__main__":
    print("🚀 Starting API server test...")
    print("Make sure the API server is running on http://localhost:8000")
    print("Run: python main.py")
    print()
    
    # Run the tests
    asyncio.run(test_two_party_api())
    asyncio.run(test_api_endpoints_overview()) 