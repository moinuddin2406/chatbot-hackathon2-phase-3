"""
Debug script to test the password hashing implementation
and verify that the fix is properly applied.
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from security import hash_password, verify_password
import hashlib

def debug_password_handling():
    print("Testing password handling with the updated implementation...")
    
    # Test with a long password
    long_password = "a" * 80  # 80 characters, longer than the 72 limit
    
    print(f"Original password length: {len(long_password)}")
    
    # Check the internal processing
    password_digest = hashlib.sha256(long_password.encode('utf-8')).hexdigest()
    print(f"SHA-256 digest length: {len(password_digest)}")
    print(f"SHA-256 digest (first 20 chars): {password_digest[:20]}")
    
    # Hash the password
    try:
        hashed = hash_password(long_password)
        print(f"Password hashed successfully!")
        print(f"Bcrypt hash (first 30 chars): {hashed[:30]}...")
        
        # Verify the password
        is_valid = verify_password(long_password, hashed)
        print(f"Password verification result: {is_valid}")
        
        if is_valid:
            print("\n[PASS] SUCCESS: The bcrypt 72-byte fix is working correctly!")
        else:
            print("\n[FAIL] ERROR: Password verification failed!")

    except Exception as e:
        print(f"\n[FAIL] ERROR: {str(e)}")
        print("The fix may not be properly implemented.")

if __name__ == "__main__":
    debug_password_handling()