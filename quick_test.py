#!/usr/bin/env python3
"""
Quick test for models only
"""

try:
    print("Testing model imports...")
    
    # Test basic imports
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    # Test enum imports
    from app.models.user import UserRole
    print("✅ UserRole imported")
    
    from app.models.common import FavoritableTypeEnum, NotificationTypeEnum
    print("✅ Common enums imported")
    
    from app.models.session import SessionTypeEnum
    print("✅ Session enums imported")
    
    print("\n🎉 Basic model imports successful!")
    
except Exception as e:
    print(f"❌ Import error: {e}")
    import traceback
    traceback.print_exc() 