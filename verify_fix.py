"""
Verification script to check if the bcrypt fix is properly implemented
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

try:
    from security import hash_password, verify_password
    import inspect
    
    print("=== Verification of bcrypt fix implementation ===")
    
    # Check the source code of the functions to ensure they're using the correct implementation
    hash_func_source = inspect.getsource(hash_password)
    verify_func_source = inspect.getsource(verify_password)
    
    print("1. Checking hash_password function:")
    if "hashlib.sha256" in hash_func_source and "hexdigest()" in hash_func_source:
        print("   [PASS] Uses SHA-256 pre-hashing as expected")
    else:
        print("   [FAIL] Does NOT use SHA-256 pre-hashing - this is the old implementation!")
        print("   Current implementation:")
        print(hash_func_source)

    print("\n2. Checking verify_password function:")
    if "hashlib.sha256" in verify_func_source and "hexdigest()" in verify_func_source:
        print("   [PASS] Uses SHA-256 pre-hashing as expected")
    else:
        print("   [FAIL] Does NOT use SHA-256 pre-hashing - this is the old implementation!")
        print("   Current implementation:")
        print(verify_func_source)

    print("\n3. Testing with a long password:")
    long_password = "a" * 80  # 80 characters, longer than the 72 limit

    try:
        hashed = hash_password(long_password)
        is_valid = verify_password(long_password, hashed)

        if is_valid:
            print("   [PASS] Long password test PASSED - fix is working correctly!")
        else:
            print("   [FAIL] Long password test FAILED - verification didn't work")
    except Exception as e:
        print(f"   [FAIL] Long password test FAILED with error: {e}")

    print("\n=== Verification complete ===")

except ImportError as e:
    print(f"Failed to import security module: {e}")
except Exception as e:
    print(f"An error occurred during verification: {e}")