from fibonacci import fibonacci
import threading 
import concurrent.futures  # 1
import socket
import sys

pool = concurrent.futures.ProcessPoolExecutor(max_workers=5)  # 2
def server(port: int):
    """Deploy a TCP/IP server on 127.0.0.1:{port}"""
    with socket.socket() as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('', port))
        sock.listen(5)
        while True:  # Accept multiple connections
            conn, addr = sock.accept()
            print(f"Established server connection on port {port} from addr {addr}")

            t = threading.Thread(target=handle, args=(conn, port, addr))
            t.start() 

def handle(conn: socket.socket, port: int, addr: str):
    with conn:
        while True:  # Accept multiple requests on the same connection
            data = conn.recv(1024)
            if not data: 
                print(f"Closed server connection on port {port} from addr {addr}")
                break
            request = int(data.decode())
            future = pool.submit(fibonacci, request)  # 3
            result = future.result()  # blocks
            response = str(result).encode() + b'\n'
            conn.send(response)

if __name__ == "__main__":
    server(int(sys.argv[1]))
