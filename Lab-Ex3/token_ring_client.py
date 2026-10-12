# Question: Token Ring Algorithm client.
# Enter the critical section only when the process receives the token, then pass the token.

import socket
import time

HOST = "127.0.0.1"
PORT = 5006
name = input("Process name: ").strip()
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
client.sendall(name.encode())

next_process = None
print("Waiting for token...")

while True:
    data = client.recv(1024).decode()
    if not data:
        break
    if data.startswith("NEXT|"):
        next_process = data.split("|", 1)[1]
    elif "TOKEN" in data:
        print(name, "entered critical section")
        time.sleep(3)
        print(name, "leaving critical section")
        if next_process:
            client.sendall(f"PASS|{next_process}".encode())
        print("Token passed to", next_process)
        break

client.close()
