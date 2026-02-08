#!/usr/bin/env python3
"""
Migration script to add missing tool_calls column to messages table
"""

import sys
import os

# Add backend to path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

from sqlalchemy import create_engine, text
from config import settings


def add_tool_calls_column():
    """Add the missing tool_calls column to the messages table"""
    print("Connecting to database...")
    
    # Create the database engine
    engine = create_engine(settings.DATABASE_URL)
    
    # Check if the column already exists
    with engine.connect() as conn:
        # Query to check if the column exists
        result = conn.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'messages' AND column_name = 'tool_calls'
        """))
        
        if result.fetchone():
            print("Column 'tool_calls' already exists in 'messages' table.")
            return True
        
        print("Column 'tool_calls' does not exist. Adding it to the 'messages' table...")
        
        try:
            # Add the tool_calls column as JSON type (can be null)
            conn.execute(text("ALTER TABLE messages ADD COLUMN tool_calls JSON"))
            conn.commit()
            print("Successfully added 'tool_calls' column to 'messages' table.")
            return True
        except Exception as e:
            print(f"Error adding column: {e}")
            conn.rollback()
            return False


if __name__ == "__main__":
    success = add_tool_calls_column()
    if success:
        print("\nMigration completed successfully!")
    else:
        print("\nMigration failed!")
        sys.exit(1)