@echo off
echo Starting the JWT-Protected Todo API backend server...
echo.

REM Change to the backend directory
cd /d "C:\Users\Moinuddin\Desktop\to-do-app_phase2\backend"

REM Activate the Python virtual environment if it exists
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
    echo Virtual environment activated.
) else (
    echo No virtual environment found, using system Python.
)

REM Install dependencies if not already installed
echo Installing/updating dependencies...
pip install -r requirements.txt

REM Initialize the database
echo Initializing database...
python -c "from db import create_db_and_tables; create_db_and_tables(); print('Database initialized successfully.')"

REM Start the server
echo Starting the server on http://127.0.0.1:8001...
python -c "
import uvicorn
from main import app

if __name__ == '__main__':
    print('Server starting on http://127.0.0.1:8001')
    print('Press Ctrl+C to stop the server')
    uvicorn.run(app, host='127.0.0.1', port=8001, log_level='info')
"