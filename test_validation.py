from backend.models import UserCreate

# Test the validation
try:
    user = UserCreate(
        name="Test User",
        email="test@example.com",
        password="a" * 80  # 80 characters, should trigger validation error
    )
    print("Validation did not catch the long password!")
    print(f"User created: {user}")
except ValueError as e:
    print(f"Validation caught the error: {e}")
except Exception as e:
    print(f"Different error: {e}")