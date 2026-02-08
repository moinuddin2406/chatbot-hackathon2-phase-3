import uvicorn
from main import app

if __name__ == '__main__':
    print('Server starting on http://127.0.0.1:8000')
    print('Press Ctrl+C to stop the server')
    print('')
    uvicorn.run(app, host='127.0.0.1', port=8000, log_level='info', reload=False)