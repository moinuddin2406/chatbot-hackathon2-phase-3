@echo off
echo Starting the JWT-Protected Todo API backend server on port 8000...
echo.

REM Change to the backend directory
cd /d "C:\Users\Moinuddin\Desktop\to-do-app_phase2\backend"
echo Current directory: %cd%

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python and ensure it's in your PATH
    pause
    exit /b 1
)

echo Python is available.

REM Install dependencies
echo.
echo Installing/updating dependencies...
pip install -r requirements.txt

REM Create database tables
echo.
echo Creating database tables...
python -c "from db import create_db_and_tables; create_db_and_tables(); print('Database tables created successfully.')"

REM Check if port is in use and kill any existing processes
echo.
echo Checking if port 8000 is in use...
netstat -ano | findstr :8000 >nul
if not errorlevel 1 (
    echo Port 8000 is in use. Finding process...
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000') do (
        echo Killing process %%a
        taskkill /PID %%a /F
    )
) else (
    echo Port 8000 is available.
)

REM Start the server on port 8000
echo.
echo Starting server on http://127.0.0.1:8000...
echo Make sure to keep this window open while using the application.
echo.
echo You can test the server at:
echo - http://127.0.0.1:8000/health (should return {\"status\": \"healthy\"})
echo - http://127.0.0.1:8000/docs (API documentation)
echo.

python -c "
import uvicorn
from main import app
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

print('Server starting on http://127.0.0.1:8000')
print('Press Ctrl+C to stop the server')
print('')

try:
    uvicorn.run(
        app, 
        host='127.0.0.1', 
        port=8000, 
        log_level='info',
        reload=False,
        timeout_keep_alive=30
    )
except KeyboardInterrupt:
    print('Server stopped by user')
except Exception as e:
    print(f'Error starting server: {e}')
    import traceback
    traceback.print_exc()
"