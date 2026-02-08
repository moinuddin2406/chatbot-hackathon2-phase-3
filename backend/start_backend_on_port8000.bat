@echo off
echo Setting up and starting the JWT-Protected Todo API backend server on port 8000...
echo.

REM Change to the backend directory (relative to this script)
cd /d "%~dp0"
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

REM Start the server using the run_server.py file
echo.
echo Starting server on http://127.0.0.1:8000...
echo Make sure to keep this window open while using the application.
echo.
echo You can test the server at:
echo - http://127.0.0.1:8000/health (should return {\"status\": \"healthy\"})
echo - http://127.0.0.1:8000/docs (API documentation)
echo.

python run_server.py