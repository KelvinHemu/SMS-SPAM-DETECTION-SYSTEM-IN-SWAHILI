#!/usr/bin/env python3
"""
Quick test of core components
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.config import get_settings
from core.logging import setup_logging
from core.ml_loader import initialize_models, get_ml_manager
from database.mock_data import get_phone_database


def test_core_components():
    """Test all core components"""
    print("=" * 50)
    print("TESTING CORE COMPONENTS")
    print("=" * 50)
    
    # Test 1: Configuration
    print("\n1. Testing Configuration...")
    try:
        settings = get_settings()
        print(f"✅ Config loaded: API Port = {settings.api_port}")
        print(f"✅ Model path: {settings.model_path}")
        print(f"✅ Confidence threshold: {settings.spam_confidence_threshold}")
    except Exception as e:
        print(f"❌ Config error: {e}")
        return False
    
    # Test 2: Logging
    print("\n2. Testing Logging...")
    try:
        setup_logging()
        print("✅ Logging configured successfully")
    except Exception as e:
        print(f"❌ Logging error: {e}")
        return False
    
    # Test 3: Phone Database
    print("\n3. Testing Phone Database...")
    try:
        phone_db = get_phone_database()
        stats = phone_db.get_stats()
        print(f"✅ Phone DB loaded: {stats['total']} records")
        print(f"   - Validated: {stats['validated']}")
        print(f"   - Flagged: {stats['flagged']}")
        
        # Test lookup
        test_phone = "0789123456"
        status = phone_db.get_phone_status(test_phone)
        print(f"✅ Test lookup {test_phone}: {status}")
        
    except Exception as e:
        print(f"❌ Phone DB error: {e}")
        return False
    
    # Test 4: ML Models (if available)
    print("\n4. Testing ML Models...")
    try:
        if os.path.exists(settings.model_path) and os.path.exists(settings.vectorizer_path):
            success = initialize_models()
            if success:
                print("✅ ML models loaded successfully")
                
                # Test prediction
                ml_manager = get_ml_manager()
                test_text = "Umeshinda milioni 50"
                prediction, confidence = ml_manager.predict_text(test_text)
                print(f"✅ Test prediction: '{test_text}' -> {prediction} ({confidence:.3f})")
            else:
                print("❌ Failed to load ML models")
                return False
        else:
            print("⚠️  ML model files not found - skipping test")
            print(f"   Expected: {settings.model_path}")
            print(f"   Expected: {settings.vectorizer_path}")
    
    except Exception as e:
        print(f"❌ ML models error: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("✅ ALL CORE COMPONENTS WORKING!")
    print("=" * 50)
    return True


if __name__ == "__main__":
    success = test_core_components()
    sys.exit(0 if success else 1) 