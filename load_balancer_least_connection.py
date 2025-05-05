from server import server  
import threading
import socket
import sys

class Router:

    def __init__(self, server_ports: list[int]): 
        self.server_connections = {
            port: 0 for port in server_ports
        }
        self.lock = threading.Lock() 

    def acquire_port(self): 
        with self.lock:
            port = min(
                self.server_connections.keys(),
                key=lambda port: self.server_connections[port]
            )
            self.server_connections[port] += 1
            return port
    
    def release_port(self, port: int): 
        with self.lock:
            self.server_connections[port] -= 1
        

def load_balancer(port: int, router: Router): 
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
                    args=(conn, port, addr, router)
                ).start()  
    except Exception as e:
        print(e)
    except BaseException:
        print("\nLoad Balancer was disconnected")

def handle(
        conn: socket.socket, port: int, addr: str,
        router: Router
):  
    server_port = router.acquire_port()  
    with conn, socket.socket() as server_conn: 
        server_conn.connect(('', server_port)) 
        while True:  # Accept multiple requests per conn 
            data = conn.recv(1024)
            if not data: 
                print(
                    "Closed load_balancer connection "
                    f"on port {port} from addr {addr}"
                )
                router.release_port(server_port)  
                break
            server_conn.sendall(data)  
            response = server_conn.recv(1024)  
            conn.send(response)

if __name__ == "__main__":
    server_ports = list(map(int, sys.argv[2:]))
    router = Router(server_ports)  
    for port in server_ports:
        threading.Thread(
            target=server, args=(port,), daemon=True
        ).start()
    load_balancer(int(sys.argv[1]), router)  
