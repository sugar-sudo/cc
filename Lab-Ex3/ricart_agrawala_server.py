# Question: Task 2 - Implement the Ricart-Agrawala algorithm using message passing.
# Processes request the CS, receive permission messages, and only one enters the CS at a time.
# This server acts only as a socket message relay; the RA decision is made by clients.

import socket
import threading

HOST = "127.0.0.1"
PORT = 5005
clients = {}
lock = threading.Lock()


def broadcast(message, sender):
    with lock:
        for name, conn in clients.items():
            if name != sender:
                try:
                    conn.sendall((message.rstrip("\n") + "\n").encode())
                except OSError:
                    pass


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
        broadcast(data.decode(), name)

    with lock:
        clients.pop(name, None)
        for c in clients.values():
            c.sendall(f"PEERS|{','.join(clients)}\n".encode())
    conn.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(10)
print("Ricart-Agrawala relay listening on", PORT)

while True:
    conn, addr = server.accept()
    threading.Thread(target=handle, args=(conn,), daemon=True).start()
