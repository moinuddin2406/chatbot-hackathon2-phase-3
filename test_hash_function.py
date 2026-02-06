import sys
sys.path.append('./backend')

from security import hash_password

# Test the hash_password function directly with a long password
long_password = "a" * 80  # 80 characters, longer than the 72 limit
try:
    hashed = hash_password(long_password)
    print("Success: Password was hashed without error")
    print(f"Original length: {len(long_password)}")
    print(f"Hashed successfully: {hashed[:20]}...")  # Show first 20 chars of hash
except Exception as e:
    print(f"Error: {e}")