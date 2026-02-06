import requests
import time

def test_server():
    url = "http://127.0.0.1:8001/health"
    try:
        print(f"Attempting to connect to {url}")
        response = requests.get(url, timeout=10)
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to server: {e}")

if __name__ == "__main__":
    test_server()