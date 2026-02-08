import subprocess
import sys

# Start the server and capture output
process = subprocess.Popen([
    sys.executable, "-m", "uvicorn", "main:app", 
    "--host", "127.0.0.1", 
    "--port", "8000"
], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
   universal_newlines=True, cwd=r"D:\hackathon\phase3-chatbot\backend")

# Read the first few lines of output
for i in range(10):  # Read first 10 lines
    try:
        output = process.stdout.readline()
        if output:
            print(output.strip())
        else:
            break
    except:
        break

# Terminate the process
process.terminate()