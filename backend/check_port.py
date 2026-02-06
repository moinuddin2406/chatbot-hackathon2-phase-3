import socket

def check_port(host, port):
    """Check if a port is available"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((host, port))
    sock.close()
    return result == 0  # 0 means connection successful (port in use)

def test_connection():
    host = '127.0.0.1'
    port = 8001
    
    print(f"Checking if server is running on {host}:{port}...")
    
    if check_port(host, port):
        print(f"✓ Port {port} is in use - server might be running")
    else:
        print(f"✗ Port {port} is not in use - server might not be running")

if __name__ == "__main__":
    test_connection()