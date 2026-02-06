import socket
import threading
import time

def start_simple_server():
    """Start a simple server to test if we can bind to the port"""
    def handle_client(conn, addr):
        print(f"Connection from {addr}")
        conn.send(b"HTTP/1.1 200 OK\n\nSimple server working!")
        conn.close()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server.bind(('127.0.0.1', 8001))
        server.listen(5)
        print("Simple server listening on 127.0.0.1:8001")
        
        # Run in a thread so we can test the connection
        def server_loop():
            while True:
                try:
                    conn, addr = server.accept()
                    handle_client(conn, addr)
                except:
                    break
        
        thread = threading.Thread(target=server_loop)
        thread.daemon = True
        thread.start()
        
        # Keep server running for a while
        time.sleep(30)
        
    except Exception as e:
        print(f"Error starting simple server: {e}")
    finally:
        server.close()

if __name__ == "__main__":
    start_simple_server()