# Question: Centralized Coordinator client.
# Request access to the CS, wait for GRANT, execute the CS, then release it.

import socket
import time

HOST = "127.0.0.1"
PORT = 5004

name = input("Process name: ").strip()
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
client.sendall(name.encode())

input("Press Enter to request the critical section...")
client.sendall(b"REQUEST")

while client.recv(1024).decode() != "GRANT":
    pass

print(name, "entered critical section")
time.sleep(3)
print(name, "leaving critical section")
client.sendall(b"RELEASE")
client.close()
