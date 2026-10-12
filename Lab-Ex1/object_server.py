# Question: Task 2 - Define DataObject(name, values), serialize/deserialize it with pickle,
# receive it on the server, compute the sum of values, and send the result back.

import socket
import pickle

HOST = "127.0.0.1"
PORT = 5002

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)
print(f"Object server listening on {HOST}:{PORT}")

conn, addr = server.accept()
with conn:
    print("Connected:", addr)
    data = conn.recv(4096)
    obj = pickle.loads(data)
    total = sum(obj["values"])
    response = f"Name: {obj['name']}, Sum: {total}"
    conn.sendall(response.encode())
