# Question: Task 1 - Create a simple socket connection where the client sends a message
# and the server responds. Bind to a host and port, listen, accept messages, and sum numbers.

import socket

HOST = "127.0.0.1"
PORT = 5001

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)
print(f"Server listening on {HOST}:{PORT}")

while True:
    conn, addr = server.accept()
    with conn:
        print("Connected:", addr)
        data = conn.recv(4096).decode()
        if not data:
            continue

        try:
            numbers = [int(x) for x in data.split()]
            result = sum(numbers)
            response = f"Sum = {result}"
        except ValueError:
            response = "Send space-separated numbers only."

        conn.sendall(response.encode())
