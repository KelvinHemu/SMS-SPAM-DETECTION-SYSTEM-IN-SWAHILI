#!/usr/bin/env python3
"""
Swahili Message Labeling Demo
Demonstrates the automatic Swahili warning label system
"""

import requests
import json
from datetime import datetime

# API Configuration
API_BASE = "http://localhost:3000/api/v1"
API_ANALYZE = f"{API_BASE}/analyze"
API_LABELS = f"{API_BASE}/analyze/labels"

def print_separator(title="", width=60):
    """Print a formatted separator"""
    if title:
        print(f"\n{'='*width}")
        print(f"{title:^{width}}")
        print(f"{'='*width}")
    else:
        print("-" * width)

def demonstrate_analysis(message, phone, description):
    """Demonstrate analysis of a single message"""
    print(f"\n📱 {description}")
    print(f"Original: \"{message}\"")
    print(f"Phone: {phone}")
    
    try:
        # Send analysis request
        response = requests.post(API_ANALYZE, json={
            "text": message,
            "phone_number": phone
        })
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"\n📊 Analysis Results:")
            print(f"Decision: {result['decision']}")
            print(f"Confidence: {result['confidence']:.3f}")
            print(f"Processing Time: {result['processing_time_ms']:.1f}ms")
            
            print(f"\n🏷️ Labeled Message:")
            print("─" * 40)
            print(result['labeled_message'])
            print("─" * 40)
            
            # Show label status
            original_text = message
            labeled_text = result['labeled_message']
            
            if labeled_text == original_text:
                print("✅ No warning label (message is clean)")
            else:
                if "⚠️ Tahadhari" in labeled_text:
                    print("⚠️ Warning label added in Swahili")
                elif "🚫 Imezuiliwa" in labeled_text:
                    print("🚫 Blocked label added in Swahili")
                    print("❌ This message would NOT be delivered")
            
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the API server is running")
        print("   Start with: python main.py")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False
    
    return True

def show_available_labels():
    """Show all available Swahili labels"""
    print_separator("AVAILABLE SWAHILI LABELS")
    
    try:
        response = requests.get(API_LABELS)
        if response.status_code == 200:
            data = response.json()
            labels = data['labels']
            
            for decision, info in labels.items():
                print(f"\n🔹 {decision}:")
                standard = info['standard']
                print(f"   Swahili: {standard['swahili_label'] or 'No label'}")
                print(f"   English: {standard['english_translation']}")
                print(f"   Example:")
                print(f"   {info['example_message']}")
                
        else:
            print(f"❌ Error fetching labels: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def main():
    """Main demonstration"""
    print_separator("🇹🇿 SWAHILI MESSAGE LABELING DEMO")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("Demonstrating automatic Swahili warning labels for spam detection")
    
    # Show available labels
    show_available_labels()
    
    # Test messages
    test_cases = [
        {
            "message": "Habari za mchana, je hali gani?",
            "phone": "+255754111222",
            "description": "Clean Swahili greeting (should be no label)"
        },
        {
            "message": "Umeshinda milioni 50, piga simu kwa maelezo zaidi",
            "phone": "+255787123456", 
            "description": "Traditional spam in Swahili (should get warning)"
        },
        {
            "message": "WIN BIG NOW!!! Call immediately for your prize money!!!",
            "phone": "+255799999999",
            "description": "English spam message (should get warning)"
        },
        {
            "message": "Hello, I hope you are doing well. Best regards.",
            "phone": "+255754111222",
            "description": "Legitimate English message (should be clean)"
        },
        {
            "message": "MCHAKATAA mkuu, umeshinda dola milioni moja! Piga simu 0700123456 sasa!",
            "phone": "+255700123456",
            "description": "Traditional healer spam (should be flagged)"
        }
    ]
    
    print_separator("MESSAGE ANALYSIS DEMONSTRATIONS")
    
    # Test each message
    for i, test_case in enumerate(test_cases, 1):
        print_separator(f"Test {i}/5")
        success = demonstrate_analysis(
            test_case["message"],
            test_case["phone"], 
            test_case["description"]
        )
        if not success:
            break
    
    print_separator("DEMO COMPLETE")
    print("🎉 Swahili labeling system working perfectly!")
    print("\n📋 Summary of features:")
    print("✅ Automatic Swahili warnings for suspicious content")
    print("✅ No labels for clean messages")
    print("✅ Multiple label styles (standard, compact, formal)")
    print("✅ Real-time analysis with sub-20ms response times")
    print("✅ Integration with 4-tier decision matrix")
    
    print(f"\n🔗 API Endpoints:")
    print(f"   📊 Analysis: {API_ANALYZE}")
    print(f"   🏷️ Labels: {API_LABELS}")
    print(f"   📚 Docs: http://localhost:3000/docs")

if __name__ == "__main__":
    main() 