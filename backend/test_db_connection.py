#!/usr/bin/env python3
"""
Test script to verify database connection to Neon
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import settings
from db import engine
from sqlmodel import select
from models import Task

def test_db_connection():
    print(f"DATABASE_URL: {settings.DATABASE_URL}")
    
    # Check if it's using the Neon database URL
    if "neon.tech" in settings.DATABASE_URL:
        print("[SUCCESS] Using Neon database")
    else:
        print("[WARNING] Not using Neon database - using fallback SQLite")
    
    try:
        # Test the database connection
        from sqlmodel import text
        from sqlalchemy import create_engine
        
        # Create a temporary engine to test connection
        temp_engine = create_engine(settings.DATABASE_URL)
        
        with temp_engine.connect() as conn:
            # Execute a simple query to test the connection
            result = conn.execute(text("SELECT 1")).fetchone()
            print(f"Database connection test result: {result}")
            
        print("[SUCCESS] Database connection successful!")
        
        # Test if we can query the tasks table
        try:
            with engine.connect() as conn:
                # Try to reflect the table structure
                from sqlalchemy import MetaData
                meta = MetaData()
                meta.reflect(bind=engine)
                
                print(f"Tables in database: {list(meta.tables.keys())}")
                
                # Try to query tasks table
                stmt = select(Task).limit(1)
                result = conn.execute(stmt)
                print("[SUCCESS] Successfully queried the tasks table")
                
        except Exception as e:
            print(f"[WARNING] Could not query tasks table: {e}")
        
    except Exception as e:
        print(f"[ERROR] Database connection failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_db_connection()