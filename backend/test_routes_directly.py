#!/usr/bin/env python3
"""
Direct test to see if the chat routes are being loaded by the main app
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import and run the main app startup logic directly
from main import CHAT_ROUTES_AVAILABLE, app

print(f"CHAT_ROUTES_AVAILABLE: {CHAT_ROUTES_AVAILABLE}")

# Print all routes registered in the app
print("\nRegistered routes:")
for route in app.routes:
    if hasattr(route, 'methods') and hasattr(route, 'path'):
        print(f"  {route.path} - {route.methods}")
    else:
        print(f"  {route}")

# Check specifically for chat routes
chat_routes = [route for route in app.routes 
               if hasattr(route, 'path') and 'chat' in route.path.lower()]
print(f"\nChat routes found: {len(chat_routes)}")
for route in chat_routes:
    print(f"  {route.path} - {route.methods}")