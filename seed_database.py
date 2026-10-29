#!/usr/bin/env python3
"""
Database seeding script for STRAUMANN Event API
Run this script to populate the database with sample data
"""

import sys
import os
import asyncio

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.seed_data import main

if __name__ == "__main__":
    print("🌱 STRAUMANN Event API - Database Seeding")
    print("=" * 50)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⚠️  Seeding interrupted by user")
    except Exception as e:
        print(f"\n❌ Seeding failed: {e}")
        sys.exit(1) 