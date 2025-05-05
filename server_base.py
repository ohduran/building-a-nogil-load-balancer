from fibonacci import fibonacci
import socket
import sys

def server(port: int):
    """Deploy a TCP/IP server on 127.0.0.1:{port}"""
    with socket.socket() as sock:
        sock.bind(('', port))
        sock.listen(5)
        while True:  # Accept multiple connections
            conn, addr = sock.accept()
            print(f"Established server connection on port {port} from addr {addr}")

            handle(conn, port, addr)

def handle(conn: socket.socket, port: int, addr: str):
    with conn:
        while True:  # Accept multiple requests on the same connection
            data = conn.recv(1024)
            if not data: 
                print(f"Closed server connection on port {port} from addr {addr}")
                break
            request = int(data.decode())
            response = str(fibonacci(request)).encode() + b'\n'
            conn.send(response)

if __name__ == "__main__":
    server(int(sys.argv[1]))
