import time
import socket
import sys
import threading

number_of_clients = int(sys.argv[2])
clients = [0] * number_of_clients


def monitor_reqs_per_second():
    global clients
    while True:
        time.sleep(1)  # 1 second
        print(clients)
        clients = [0] * int(sys.argv[2])

def test(client_id: int):
    global clients
    port = int(sys.argv[1])
    with socket.socket() as sock:
        sock.connect(('', port))  # connect to the port
        while True:
            sock.send(b'30')
            sock.recv(1024)
            clients[client_id] += 1

for client_id in range(number_of_clients):
    t = threading.Thread(target=test, args=(client_id,), daemon=True)
    t.start()

u = threading.Thread(target=monitor_reqs_per_second)
u.start()
