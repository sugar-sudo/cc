# Question: Task 1 and Task 2 - Use message passing to exchange timestamps.
# The server relays messages between distributed processes. Logical/vector clock updates
# are performed by each client process when sending and receiving messages.

import socket
import threading

HOST = "127.0.0.1"
PORT = 5007
clients = {}
lock = threading.Lock()


def handle(conn):
    name = conn.recv(1024).decode().strip()
    with lock:
        clients[name] = conn
        peers = ",".join(clients)
        for c in clients.values():
            c.sendall(f"PEERS|{peers}\n".encode())

    while True:
        data = conn.recv(4096)
        if not data:
            break
        with lock:
            for peer, c in clients.items():
                if peer != name:
                    try:
                        c.sendall(data)
                    except OSError:
                        pass

    with lock:
        clients.pop(name, None)
    conn.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(10)
print("Clock server listening on", PORT)

while True:
    conn, addr = server.accept()
    threading.Thread(target=handle, args=(conn,), daemon=True).start()
