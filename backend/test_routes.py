import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.getcwd())

print("Attempting to import routes...")

try:
    from routes import tasks
    print("Routes imported successfully!")
    
    # Check if the router exists
    if hasattr(tasks, 'router'):
        print("Router attribute exists")
    else:
        print("Router attribute does not exist")
        
except Exception as e:
    print(f"Error importing routes: {e}")
    import traceback
    traceback.print_exc()

print("Done.")