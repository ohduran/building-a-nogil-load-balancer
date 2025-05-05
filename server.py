from fibonacci import fibonacci
import threading 
import socket
import sys

def server(port: int):
    """Deploy a TCP/IP server on 127.0.0.1:{port}"""
    try:
        with socket.socket() as sock:
            sock.setsockopt(
                socket.SOL_SOCKET, socket.SO_REUSEADDR, 1
            )
            sock.bind(('', port))
            sock.listen(5)
            while True:  # Accept multiple connections
                conn, addr = sock.accept()
                print(
                    "Established server connection "
                    f"on port {port} from addr {addr}"
                )
                threading.Thread(
                    target=handle,
                   args=(conn, port, addr)
                ).start()
    except Exception as e:
        print(e)
    except BaseException:
        print("\nServer was disconnected")

def handle(conn: socket.socket, port: int, addr: str):
    with conn:
        while True:  # Accept multiple requests per conn 
            data = conn.recv(1024)
            if not data: 
                print(
                    "Closed server connection "
                    f"on port {port} from addr {addr}"
                )
                break
            request = int(data.decode())
            response = str(fibonacci(request)).encode() 
            conn.send(response + b'\n')

if __name__ == "__main__":
    server(int(sys.argv[1]))
