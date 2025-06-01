# Two-Party Messaging System

## Overview

The spam detection system now supports a **two-party messaging flow** where messages are sent from a **Sender** to a **Receiver** through our analysis and delivery system.

## Message Flow

```
👤 SENDER → 🔍 SYSTEM ANALYSIS → 👤 RECEIVER
```

### Process Steps

1. **Message Reception**: Sender sends message intended for receiver
2. **Sender Validation**: System checks sender's phone number reputation
3. **Content Analysis**: ML model classifies message content (spam/ham)
4. **Decision Making**: Combined analysis determines final outcome
5. **Label Addition**: Suspicious messages get Swahili warning labels
6. **Delivery Decision**: System delivers, labels, or blocks message
7. **Final Delivery**: Receiver gets processed message (if not blocked)

## API Request Format

The new request format includes both sender and receiver information:

```json
{
  "text": "Message content to analyze",
  "sender_phone": "+255712345678",
  "receiver_phone": "+255787654321"
}
```

### Example Requests

**Clean Message:**
```bash
curl -X POST "http://localhost:8000/api/v1/analyze" \
     -H "Content-Type: application/json" \
     -d '{
       "text": "Habari za mchana, je hali gani?",
       "sender_phone": "+255712345678",
       "receiver_phone": "+255787654321"
     }'
```

**Suspicious Content:**
```bash
curl -X POST "http://localhost:8000/api/v1/analyze" \
     -H "Content-Type: application/json" \
     -d '{
       "text": "Umeshinda milioni 50, piga simu kwa maelezo zaidi",
       "sender_phone": "+255765432108",
       "receiver_phone": "+255787654321"
     }'
```

## Decision Outcomes & Delivery

| Decision | Description | Delivery Action |
|----------|-------------|-----------------|
| `CLEAN` | Safe message from trusted source | ✅ Deliver as-is |
| `CONTENT_WARNING` | Suspicious content detected | ⚠️ Deliver with warning label |
| `SENDER_WARNING` | Suspicious sender reputation | ⚠️ Deliver with warning label |
| `BLOCKED` | High confidence spam | 🚫 Block delivery completely |

## Response Format

The API response now includes comprehensive delivery information:

```json
{
  "message_id": "msg_1a2b3c4d5e6f",
  "decision": "CONTENT_WARNING",
  "confidence": 0.75,
  "sender_phone": "+255712345678",
  "receiver_phone": "+255787654321",
  "text_classification": "spam",
  "text_confidence": 0.82,
  "phone_status": "validated",
  "phone_risk_score": 0.15,
  "original_message": "Umeshinda milioni 50, piga simu...",
  "labeled_message": "⚠️ Onyo: SPAM\n\nUmeshinda milioni 50, piga simu...",
  "delivery_result": {
    "delivery_id": "del_9f8e7d6c5b4a",
    "status": "delivered",
    "delivered_message": "⚠️ Onyo: SPAM\n\nUmeshinda milioni 50, piga simu...",
    "delivery_time": "2024-01-15T10:30:45.123Z",
    "error_message": null
  },
  "reasoning": "Message contains lottery/prize content with moderate confidence. Sender has good reputation.",
  "processing_time_ms": 45.7,
  "timestamp": "2024-01-15T10:30:45.123Z"
}
```

## New API Endpoints

### 1. Message Analysis & Delivery
**POST** `/api/v1/analyze`

Analyzes sender-to-receiver message and handles delivery.

### 2. Test Endpoint
**GET** `/api/v1/analyze/test`

Tests the two-party flow with predefined sender and receiver.

### 3. Delivery Statistics
**GET** `/api/v1/analyze/stats/delivery`

Returns comprehensive delivery and system statistics:

```json
{
  "delivery_performance": {
    "total_deliveries": 25,
    "successful_deliveries": 18,
    "blocked_messages": 5,
    "failed_deliveries": 2,
    "success_rate": 72.0
  },
  "message_decisions": {
    "CLEAN": 12,
    "CONTENT_WARNING": 8,
    "SENDER_WARNING": 3,
    "BLOCKED": 2
  },
  "system_health": {
    "status": "healthy",
    "components_healthy": {
      "text_classification": true,
      "phone_validation": true,
      "decision_engine": true,
      "message_delivery": true
    },
    "uptime_seconds": 3600.5
  },
  "two_party_flow_info": {
    "description": "Sender → System Analysis → Receiver (if not blocked)",
    "decision_flow": {
      "CLEAN": "Message delivered as-is",
      "CONTENT_WARNING": "Message delivered with warning label",
      "SENDER_WARNING": "Message delivered with sender warning",
      "BLOCKED": "Message blocked, no delivery"
    }
  }
}
```

## Swahili Warning Labels

Messages with warnings get appropriate Swahili labels:

| Scenario | Label Added |
|----------|-------------|
| Content Warning | `⚠️ Onyo: SPAM` |
| Sender Warning | `⚠️ Onyo: Mtumaji wa shaka` |
| Blocked | `🚫 Imezuiliwa: SPAM` |

## Testing the System

### 1. Unit Testing
```bash
python test_two_party_messaging.py
```

### 2. API Testing
```bash
# Start the server
python main.py

# In another terminal
python test_two_party_api.py
```

### 3. Manual Testing
Use the FastAPI docs at `http://localhost:8000/docs` to test endpoints interactively.

## Integration Examples

### Python Integration
```python
import asyncio
import httpx

async def send_message(sender, receiver, text):
    """Send message through spam detection system"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/v1/analyze",
            json={
                "text": text,
                "sender_phone": sender,
                "receiver_phone": receiver
            }
        )
        return response.json()

# Example usage
result = asyncio.run(send_message(
    sender="+255712345678",
    receiver="+255787654321", 
    text="Habari za mchana, je hali gani?"
))

print(f"Decision: {result['decision']}")
print(f"Delivered: {result['delivery_result']['status'] == 'delivered'}")
```

### cURL Examples
```bash
# Clean message
curl -X POST "http://localhost:8000/api/v1/analyze" \
     -H "Content-Type: application/json" \
     -d '{"text": "Hello, how are you?", "sender_phone": "+255712345678", "receiver_phone": "+255787654321"}'

# Check delivery stats
curl "http://localhost:8000/api/v1/analyze/stats/delivery"

# Health check
curl "http://localhost:8000/api/v1/health"
```

## Production Considerations

### SMS Gateway Integration
In production, replace the simulation in `MessageDeliveryService._simulate_sms_delivery()` with actual SMS gateway integration:

```python
async def _integrate_sms_gateway(self, receiver_phone, message_text, sender_phone):
    """Integrate with real SMS gateway"""
    # Example integration points:
    # - Twilio SMS API
    # - AWS SNS
    # - Africa's Talking SMS
    # - Local telecom provider APIs
    
    gateway_response = await sms_provider.send_message(
        to=receiver_phone,
        from_=sender_phone,
        body=message_text
    )
    
    return gateway_response.success
```

### Database Scaling
For high-volume production use:
- Replace SQLite with PostgreSQL/MySQL
- Implement phone number caching
- Add message history tracking
- Use async database drivers

### Performance Optimization
- Implement request queuing for high loads
- Add Redis caching for phone validations
- Use background tasks for delivery retries
- Monitor delivery success rates

## Monitoring & Analytics

The system provides comprehensive monitoring:

1. **Delivery Success Rates**: Track message delivery performance
2. **Decision Distribution**: Monitor spam detection accuracy  
3. **Sender Reputation**: Track phone number risk scores
4. **Processing Performance**: Monitor response times
5. **System Health**: Component status monitoring

## Security Features

1. **Phone Number Validation**: Validates sender reputation
2. **Content Filtering**: ML-powered spam detection
3. **Rate Limiting**: Prevent abuse (configure in production)
4. **Audit Logging**: All decisions are logged and traceable
5. **Configurable Thresholds**: Adjust sensitivity as needed

## Summary

The two-party messaging system provides a complete SMS filtering solution that:

- ✅ Validates sender reputation
- ✅ Analyzes message content with ML
- ✅ Makes intelligent delivery decisions
- ✅ Adds appropriate warning labels
- ✅ Provides comprehensive monitoring
- ✅ Supports both English and Swahili content
- ✅ Offers production-ready architecture

This system can be easily integrated into existing messaging platforms, SMS gateways, or communication systems. 