"""
Test script to verify the bcrypt 72-byte limitation solution.
This tests both hashing and verification with long passwords.
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from security import hash_password, verify_password

def test_short_password():
    """Test with a short password (< 72 characters)"""
    password = "short_password_123"
    hashed = hash_password(password)
    assert verify_password(password, hashed), "Short password verification failed"
    print("[PASS] Short password test passed")


def test_long_password():
    """Test with a long password (> 72 characters)"""
    password = "a" * 80  # 80 characters, longer than the 72 limit
    hashed = hash_password(password)
    assert verify_password(password, hashed), "Long password verification failed"
    print("[PASS] Long password test passed")


def test_very_long_password():
    """Test with a very long password (e.g., 200 characters)"""
    password = "x" * 200  # 200 characters
    hashed = hash_password(password)
    assert verify_password(password, hashed), "Very long password verification failed"
    print("[PASS] Very long password test passed")


def test_different_passwords():
    """Test that different passwords don't match the same hash"""
    password1 = "password_one_that_is_reasonably_long_to_test_the_bcrypt_limitations"
    password2 = "password_two_that_is_reasonably_long_to_test_the_bcrypt_limitations"
    
    hashed1 = hash_password(password1)
    assert not verify_password(password2, hashed1), "Different passwords should not match"
    print("[PASS] Different passwords test passed")


def test_special_characters():
    """Test with special characters and unicode"""
    password = "p@ssw0rd_w1th_$p3c!@l_ch@rs_αβγδεζηθικλμνξοπρστυφχψω_🎉🚀🌟"
    hashed = hash_password(password)
    assert verify_password(password, hashed), "Special character password verification failed"
    print("[PASS] Special characters password test passed")


if __name__ == "__main__":
    print("Testing bcrypt 72-byte limitation solution...")
    test_short_password()
    test_long_password()
    test_very_long_password()
    test_different_passwords()
    test_special_characters()
    print("\n[PASS] All tests passed! The bcrypt 72-byte limitation solution is working correctly.")