@echo off
echo Diagnosing and fixing backend loading issues...
echo.

REM Change to the backend directory
cd /d "C:\Users\Moinuddin\Desktop\to-do-app_phase2\backend"

echo 1. Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo.
echo 2. Checking required packages...
pip list | findstr -i "fastapi uvicorn sqlmodel pyjwt passlib"
if errorlevel 1 (
    echo Installing missing packages...
    pip install -r requirements.txt
)

echo.
echo 3. Checking if port 8001 is in use...
netstat -an | findstr :8001
if not errorlevel 1 (
    echo Port 8001 is in use. Checking process...
    netstat -ano | findstr :8001
    echo If you see a process using this port, you may need to stop it.
) else (
    echo Port 8001 is available.
)

echo.
echo 4. Testing database connection...
python -c "
import sqlite3
import os
from config import settings

try:
    db_path = settings.DATABASE_URL.replace('sqlite:///', '')
    print(f'Testing database connection to: {db_path}')
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT 1')
    print('✓ Database connection successful')
    conn.close()
except Exception as e:
    print(f'✗ Database connection failed: {e}')
"

echo.
echo 5. Testing imports...
python -c "
try:
    import fastapi
    import uvicorn
    from main import app
    from config import settings
    from db import create_db_and_tables
    print('✓ All imports successful')
except Exception as e:
    print(f'✗ Import error: {e}')
    import traceback
    traceback.print_exc()
"

echo.
echo 6. Creating database tables...
python -c "
try:
    from db import create_db_and_tables
    create_db_and_tables()
    print('✓ Database tables created successfully')
except Exception as e:
    print(f'✗ Error creating database tables: {e}')
    import traceback
    traceback.print_exc()
"

echo.
echo 7. Attempting to start server in background...
start /min python -c "
import uvicorn
from main import app
import time

print('Server starting on http://127.0.0.1:8001')
print('Check http://127.0.0.1:8001/health in a moment')
try:
    uvicorn.run(app, host='127.0.0.1', port=8001, log_level='info', reload=False)
except Exception as e:
    print(f'Server startup error: {e}')
    import traceback
    traceback.print_exc()
input('Press Enter to exit...')
"

echo.
echo 8. Waiting 10 seconds for server to start...
timeout /t 10 /nobreak >nul

echo.
echo 9. Testing server connection...
powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://127.0.0.1:8001/health' -Method GET; Write-Host '✓ Server is responding'; Write-Host 'Response:' $response.Content } catch { Write-Host '✗ Server is not responding' }"

echo.
echo Diagnostic complete. Check the output above for any errors.
echo If the server is running, you should be able to access http://127.0.0.1:8001/health
pause