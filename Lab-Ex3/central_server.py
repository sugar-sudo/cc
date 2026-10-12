# Question: Task 2 - Centralized Coordinator Algorithm.
# Processes request the critical section (CS) by messages; only one process enters CS at a time.
# The coordinator grants and releases access to the CS.

import socket
import threading

HOST = "127.0.0.1"
PORT = 5004
queue = []
current = None
clients = {}
lock = threading.Lock()


def send(conn, text):
    conn.sendall(text.encode())


def try_grant():
    global current
    with lock:
        if current is None and queue:
            current = queue.pop(0)
            send(clients[current], "GRANT")
            print("Granted CS to", current)


def handle(conn, addr):
    global current
    name = conn.recv(1024).decode().strip()
    with lock:
        clients[name] = conn
    print(name, "connected")

    try:
        while True:
            msg = conn.recv(1024).decode().strip()
            if not msg:
                break
            with lock:
                if msg == "REQUEST" and name != current and name not in queue:
                    queue.append(name)
                elif msg == "RELEASE" and name == current:
                    current = None
            try_grant()
    finally:
        with lock:
            clients.pop(name, None)
            if name in queue:
                queue.remove(name)
            if name == current:
                current = None
        try_grant()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(10)
print("Central coordinator listening on", PORT)

while True:
    conn, addr = server.accept()
    threading.Thread(target=handle, args=(conn, addr), daemon=True).start()
