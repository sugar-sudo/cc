# Question: Task 1 - Create a server that accepts multiple clients via sockets.
# Each client can send and receive messages so distributed processes can communicate.

import socket
import threading

HOST = "127.0.0.1"
PORT = 5003
clients = []
lock = threading.Lock()


def handle_client(conn, addr):
    with lock:
        clients.append(conn)
    print("Connected:", addr)

    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            message = data.decode()
            print(addr, ">", message)
            with lock:
                for client in clients:
                    if client != conn:
                        client.sendall(f"{addr}: {message}".encode())
    finally:
        with lock:
            if conn in clients:
                clients.remove(conn)
        conn.close()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(10)
print(f"Message server listening on {PORT}")

while True:
    conn, addr = server.accept()
    threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
