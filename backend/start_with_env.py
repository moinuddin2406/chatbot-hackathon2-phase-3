import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file in the parent directory
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path)

# Now import and run the main app
from main import app
import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)