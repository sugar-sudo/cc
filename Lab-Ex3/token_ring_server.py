# Question: Task 2 - Implement the Token Ring Algorithm.
# Processes form a logical ring. A process enters the CS only when it holds the token.
# After releasing the CS, the token is passed to the next process.

import socket
import threading

HOST = "127.0.0.1"
PORT = 5006
clients = {}
lock = threading.Lock()


def send_to(name, message):
    with lock:
        if name in clients:
            clients[name].sendall(message.encode())


def handle(conn):
    name = conn.recv(1024).decode().strip()
    with lock:
        clients[name] = conn
        names = list(clients)
        next_name = names[(names.index(name) + 1) % len(names)]
        conn.sendall(f"NEXT|{next_name}".encode())
        if len(names) == 1:
            conn.sendall(b"TOKEN")

    while True:
        data = conn.recv(1024).decode().strip()
        if not data:
            break
        if data.startswith("PASS|"):
            send_to(data.split("|", 1)[1], "TOKEN")

    with lock:
        clients.pop(name, None)
    conn.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(10)
print("Token Ring server listening on", PORT)

while True:
    conn, addr = server.accept()
    threading.Thread(target=handle, args=(conn,), daemon=True).start()
