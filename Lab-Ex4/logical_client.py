# Question: Task 1 - Lamport's Logical Clock.
# Initialize a logical clock. Increment it for local/send events. On message receipt,
# update the clock using max(local clock, received timestamp) + 1.

import socket
import threading

HOST = "127.0.0.1"
PORT = 5007
name = input("Process name: ").strip()
clock = 0

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
client.sendall(name.encode())


def receive():
    global clock
    while True:
        data = client.recv(4096).decode()
        if not data:
            break
        for msg in data.splitlines():
            if msg.startswith("EVENT|"):
                _, sender, timestamp, text = msg.split("|", 3)
                clock = max(clock, int(timestamp)) + 1
                print(f"Received from {sender}: {text} -> Lamport clock = {clock}")

threading.Thread(target=receive, daemon=True).start()

while True:
    text = input("Event/message (quit to stop): ")
    if text.lower() == "quit":
        break
    clock += 1
    client.sendall(f"EVENT|{name}|{clock}|{text}\n".encode())
    print("Sent with Lamport timestamp:", clock)

client.close()
