#!/usr/bin/env python3
"""
Simple script to use the exported spam detection model
"""

import joblib
import json

def load_spam_model():
    """Load the exported spam detection model and vectorizer"""
    try:
        model = joblib.load('saved_models/spam_classifier_model.pkl')
        vectorizer = joblib.load('saved_models/vectorizer.pkl')
        
        # Load metadata for reference
        with open('saved_models/model_metadata.json', 'r') as f:
            metadata = json.load(f)
        
        print("✅ Model loaded successfully!")
        print(f"Model accuracy: {metadata['accuracy']:.3f}")
        print(f"Trained on {metadata['training_samples']} samples")
        print("-" * 40)
        
        return model, vectorizer
    except FileNotFoundError:
        print("❌ Model files not found. Please run export_model.py first.")
        return None, None

def predict_message(model, vectorizer, message):
    """Predict if a message is spam or ham"""
    # Transform the message
    message_vector = vectorizer.transform([message])
    
    # Get prediction and probability
    prediction = model.predict(message_vector)[0]
    probabilities = model.predict_proba(message_vector)[0]
    
    # Get confidence score
    confidence = probabilities.max()
    
    return prediction, confidence

def main():
    # Load the model
    model, vectorizer = load_spam_model()
    if model is None:
        return
    
    # Test with some messages
    test_messages = [
        "Umeshinda milioni 20, tuma taarifa zako sasa",
        "Habari ya asubuhi, umeamka vizuri?",
        "Tuma tsh 50000 ili ushinde bahati nasibu",
        "Tutaonana shuleni kesho asubuhi",
        "MALIPO YAKO YAMEZUIWA BONYEZA LINK"
    ]
    
    print("SPAM DETECTION RESULTS:")
    print("=" * 50)
    
    for i, message in enumerate(test_messages, 1):
        prediction, confidence = predict_message(model, vectorizer, message)
        
        # Format output
        status = "🚨 SPAM" if prediction == 'spam' else "✅ HAM"
        
        print(f"{i}. {status}")
        print(f"   Message: {message[:60]}...")
        print(f"   Prediction: {prediction}")
        print(f"   Confidence: {confidence:.3f}")
        print()
    
    # Interactive mode
    print("=" * 50)
    print("🔍 INTERACTIVE MODE - Type messages to classify")
    print("(Type 'quit' to exit)")
    print("-" * 50)
    
    while True:
        try:
            user_message = input("\nEnter message: ").strip()
            if user_message.lower() in ['quit', 'exit', 'q']:
                break
            
            if user_message:
                prediction, confidence = predict_message(model, vectorizer, user_message)
                status = "🚨 SPAM" if prediction == 'spam' else "✅ HAM"
                print(f"Result: {status} (confidence: {confidence:.3f})")
        
        except KeyboardInterrupt:
            break
    
    print("\n👋 Goodbye!")

if __name__ == "__main__":
    main() 