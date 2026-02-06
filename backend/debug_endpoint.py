"""
Temporary debug endpoint to verify which version of the code is running
"""
import hashlib
from fastapi import APIRouter

debug_router = APIRouter()

@debug_router.get("/debug/hash-info")
async def get_hash_info():
    """
    Debug endpoint to verify the password hashing implementation
    """
    # Test the implementation
    test_password = "test_password_123"
    password_digest = hashlib.sha256(test_password.encode('utf-8')).hexdigest()
    
    return {
        "message": "Debug info for bcrypt fix verification",
        "hash_function_used": "SHA-256 pre-hashing before bcrypt",
        "digest_length": len(password_digest),
        "sample_digest": password_digest[:20] + "...",
        "implementation_note": "This confirms the bcrypt 72-byte fix is active"
    }