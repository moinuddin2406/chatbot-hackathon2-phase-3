#!/usr/bin/env python3
"""
Test script to verify chat routes are being loaded properly
"""

import os
import sys
import importlib.util

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_chat_route_import():
    print("Testing chat route import...")
    
    try:
        # Try to import the chat routes directly
        from chatbot.routes.chat_routes import router
        print("✓ Successfully imported chat routes")
        print(f"Router: {router}")
        print(f"Router routes: {router.routes}")
        
        # Check if the specific chat endpoint exists
        chat_endpoint_found = False
        for route in router.routes:
            if hasattr(route, 'methods') and hasattr(route, 'path'):
                print(f"  - Path: {route.path}, Methods: {route.methods}")
                if "/{user_id}/chat" in route.path and "POST" in route.methods:
                    chat_endpoint_found = True
                    
        if chat_endpoint_found:
            print("✓ Chat endpoint (/api/{user_id}/chat) found")
        else:
            print("✗ Chat endpoint not found")
            
    except ImportError as e:
        print(f"✗ Failed to import chat routes: {e}")
        import traceback
        traceback.print_exc()
    except Exception as e:
        print(f"✗ Error testing chat routes: {e}")
        import traceback
        traceback.print_exc()

def test_main_app():
    print("\nTesting main app chat route inclusion...")
    
    try:
        # Import the main app to see if chat routes are included
        from main import CHAT_ROUTES_AVAILABLE
        print(f"CHAT_ROUTES_AVAILABLE: {CHAT_ROUTES_AVAILABLE}")
        
        if CHAT_ROUTES_AVAILABLE:
            print("✓ Chat routes are marked as available in main app")
        else:
            print("✗ Chat routes are not available in main app")
            
    except Exception as e:
        print(f"✗ Error testing main app: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_chat_route_import()
    test_main_app()