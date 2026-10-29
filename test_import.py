#!/usr/bin/env python3
"""
Test script to check all imports work correctly
"""

try:
    print("Testing imports...")
    
    # Test core imports
    from app.core.config import settings
    print("✅ Core config imported")
    
    from app.core.database import Base, engine, get_db
    print("✅ Database imported")
    
    from app.core.security import get_password_hash, verify_password
    print("✅ Security imported")
    
    # Test model imports
    from app.models.user import User, UserRole
    print("✅ User model imported")
    
    from app.models.event import Event
    print("✅ Event model imported")
    
    from app.models.speaker import Speaker
    print("✅ Speaker model imported")
    
    from app.models.session import Session
    print("✅ Session model imported")
    
    from app.models.common import Favorite, Notification
    print("✅ Common models imported")
    
    # Test schema imports
    from app.schemas.user import UserCreate, UserUpdate, UserResponse
    print("✅ User schemas imported")
    
    # Test CRUD imports
    from app.crud.user import user_crud
    print("✅ User CRUD imported")
    
    # Test dependencies
    from app.core.dependencies import get_current_user
    print("✅ Dependencies imported")
    
    # Test API imports
    from app.api.v1.auth import router
    print("✅ Auth API imported")
    
    # Test main app
    from app.main import app
    print("✅ Main app imported")
    
    print("\n🎉 All imports successful!")
    
except Exception as e:
    print(f"❌ Import error: {e}")
    import traceback
    traceback.print_exc() 