#!/usr/bin/env python3
"""
Test script to check if main app loads chat routes properly
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_main_app():
    print("Testing main app startup...")
    
    try:
        # Import the main app to see if chat routes are included
        from main import CHAT_ROUTES_AVAILABLE
        print(f"CHAT_ROUTES_AVAILABLE: {CHAT_ROUTES_AVAILABLE}")
        
        if CHAT_ROUTES_AVAILABLE:
            print("✓ Chat routes are marked as available in main app")
        else:
            print("✗ Chat routes are not available in main app")
            
            # Try to import chat routes directly to see the error
            try:
                from chatbot.routes.chat_routes import router
                print("✓ Direct import of chat routes succeeded")
            except Exception as e:
                print(f"✗ Direct import of chat routes failed: {e}")
                import traceback
                traceback.print_exc()
                
    except Exception as e:
        print(f"✗ Error testing main app: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_main_app()