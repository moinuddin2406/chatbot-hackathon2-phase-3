#!/usr/bin/env python3
"""Simple test script to check if imports work properly"""

print("Testing imports...")

try:
    from main import app
    print("✓ Successfully imported app from main")
except Exception as e:
    print(f"✗ Failed to import app from main: {e}")

try:
    from config import settings
    print("✓ Successfully imported settings from config")
    print(f"  - BETTER_AUTH_SECRET set: {'Yes' if settings.BETTER_AUTH_SECRET else 'No'}")
    print(f"  - DATABASE_URL set: {'Yes' if settings.DATABASE_URL else 'No'}")
except Exception as e:
    print(f"✗ Failed to import settings from config: {e}")

try:
    from db import engine
    print("✓ Successfully imported database engine")
except Exception as e:
    print(f"✗ Failed to import database engine: {e}")

try:
    from routes import tasks
    print("✓ Successfully imported tasks from routes")
except Exception as e:
    print(f"✗ Failed to import tasks from routes: {e}")

print("\nImport test completed.")