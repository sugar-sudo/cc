# Question: Task 1 - Each client should send and receive messages using sockets.

import socket
import threading

HOST = "127.0.0.1"
PORT = 5003

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))


def receive():
    while True:
        try:
            print("\nReceived:", client.recv(4096).decode())
        except:
            break

threading.Thread(target=receive, daemon=True).start()

while True:
    message = input("Message (quit to stop): ")
    if message.lower() == "quit":
        break
    client.sendall(message.encode())

client.close()
