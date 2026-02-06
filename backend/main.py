from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from routes import tasks
from routes import auth
from config import settings
from db import create_db_and_tables
import os
import hashlib

# Create the FastAPI application instance
app = FastAPI(
    title="JWT-Protected Todo API",
    description="A secure, JWT-protected REST API for managing user tasks",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # Add exposed headers to allow frontend to access authorization headers
    expose_headers=["Authorization"]
)

# Create database tables on startup
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Include the auth routes
app.include_router(auth.router, prefix="/auth", tags=["auth"])

# Include the task routes with the proper prefix
app.include_router(tasks.router, prefix="/api/{user_id}", tags=["tasks"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the JWT-Protected Todo API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Import at the top level to avoid issues in Hugging Face environment
from security import hash_password, verify_password
import inspect

@app.get("/debug/verification")
def verification_endpoint():
    """Debug endpoint to verify the bcrypt fix is properly deployed"""
    import sys

    # Test the implementation
    test_password = "test_password_longer_than_72_chars_" + "x" * 50  # Total > 72 chars
    try:
        hashed = hash_password(test_password)
        is_valid = verify_password(test_password, hashed)

        hash_func_source = inspect.getsource(hash_password)
        verify_func_source = inspect.getsource(verify_password)

        has_sha_prehash = "hashlib.sha256" in hash_func_source and "hexdigest()" in hash_func_source
        verify_has_sha_prehash = "hashlib.sha256" in verify_func_source and "hexdigest()" in verify_func_source

        return {
            "fix_deployed": has_sha_prehash and verify_has_sha_prehash,
            "long_password_test_passed": is_valid,
            "hash_function_uses_sha_prehash": has_sha_prehash,
            "verify_function_uses_sha_prehash": verify_has_sha_prehash,
            "test_password_length": len(test_password),
            "python_version": sys.version,
            "message": "Bcrypt 72-byte fix verification" if has_sha_prehash else "Old implementation detected!"
        }
    except Exception as e:
        return {
            "fix_deployed": False,
            "error": str(e),
            "message": "Error during bcrypt fix verification"
        }

@app.get("/debug/detailed")
def detailed_debug_endpoint():
    """More detailed debug endpoint to help troubleshoot the bcrypt issue"""
    import inspect
    from security import hash_password, verify_password
    import os

    # Get the actual file path where the security module is located
    security_module_file = inspect.getfile(hash_password)

    # Get the source code of the functions
    hash_func_source = inspect.getsource(hash_password)
    verify_func_source = inspect.getsource(verify_password)

    # Check if the fix is implemented
    has_sha_prehash = "hashlib.sha256" in hash_func_source and "hexdigest()" in hash_func_source
    verify_has_sha_prehash = "hashlib.sha256" in verify_func_source and "hexdigest()" in verify_func_source

    return {
        "security_module_location": security_module_file,
        "working_directory": os.getcwd(),
        "hash_function_has_sha_prehash": has_sha_prehash,
        "verify_function_has_sha_prehash": verify_has_sha_prehash,
        "hash_function_source_preview": hash_func_source[:200] + "...",
        "verify_function_source_preview": verify_func_source[:200] + "...",
        "environment": dict(os.environ),
        "fix_correctly_implemented": has_sha_prehash and verify_has_sha_prehash
    }

# Add global exception handlers for common HTTP errors
@app.exception_handler(401)
async def unauthorized_exception_handler(request, exc):
    # Don't apply custom message to auth endpoints
    if request.url.path.startswith('/auth'):
        # Return the original exception detail
        detail = getattr(exc, 'detail', 'Unauthorized')
        return JSONResponse(
            status_code=401,
            content={"detail": detail}
        )
    return JSONResponse(
        status_code=401,
        content={"detail": "Unauthorized: Invalid or missing JWT token"}
    )

@app.exception_handler(403)
async def forbidden_exception_handler(request, exc):
    return JSONResponse(
        status_code=403,
        content={"detail": "Forbidden: User ID mismatch"}
    )