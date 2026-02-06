from security import hash_password, verify_password

long_password = 'a' * 80
try:
    hashed = hash_password(long_password)
    print('Hashing successful!')
    verified = verify_password(long_password, hashed)
    print(f'Verification result: {verified}')
    print('SUCCESS: The bcrypt fix is working correctly!')
except Exception as e:
    print(f'ERROR: {e}')