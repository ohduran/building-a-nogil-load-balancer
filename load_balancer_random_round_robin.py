import random 
from server import server 
import threading
import socket
import sys

        

def load_balancer(port: int, server_ports: list[int]): 
    """Deploy a TCP/IP load_balancer on 127.0.0.1:{port}"""
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
                    "Established load_balancer connection "
                    f"on port {port} from addr {addr}"
                )
                threading.Thread(
                    target=handle,
                    args=(conn, port, addr, server_ports)
                ).start() 
    except Exception as e:
        print(e)
    except BaseException:
        print("\nLoad Balancer was disconnected")

def handle(conn: socket.socket, port: int, addr: str,
           server_ports: list[int]
    ): 
    server_port = random.choice(server_ports)
    with conn, socket.socket() as server_conn: 
        server_conn.connect(('', server_port)) 
        while True:  # Accept multiple requests per conn 
            data = conn.recv(1024)
            if not data: 
                print(
                    "Closed load_balancer connection "
                    f"on port {port} from addr {addr}"
                )
                break
            server_conn.sendall(data) 
            response = server_conn.recv(1024) 
            conn.send(response)

if __name__ == "__main__":
    server_ports = list(map(int, sys.argv[2:]))
    for port in server_ports:
        threading.Thread(
            target=server, args=(port,), daemon=True
        ).start()
    load_balancer(int(sys.argv[1]), server_ports)
