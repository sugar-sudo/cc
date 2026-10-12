# Question: Task 2 - Vector Clocks.
# Each process keeps a vector for all processes. Increment its own entry before a send.
# On receipt, update the local vector using element-wise max, then increment own entry.

import socket
import threading

HOST = "127.0.0.1"
PORT = 5007
name = input("Process name: ").strip()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
client.sendall(name.encode())

peers = []
vector = {}
lock = threading.Lock()


def receive():
    global peers, vector
    while True:
        data = client.recv(4096).decode()
        if not data:
            break
        for msg in data.splitlines():
            if msg.startswith("PEERS|"):
                peers = sorted(filter(None, msg.split("|", 1)[1].split(",")))
                with lock:
                    for p in peers:
                        vector.setdefault(p, 0)
                    vector.setdefault(name, 0)
                print("Processes:", peers)
            elif msg.startswith("EVENT|"):
                _, sender, values, text = msg.split("|", 3)
                received = dict(item.split(":") for item in values.split(","))
                with lock:
                    for p in set(vector) | set(received):
                        vector[p] = max(vector.get(p, 0), int(received.get(p, 0)))
                    vector[name] += 1
                    current = dict(vector)
                print(f"Received from {sender}: {text} -> Vector = {current}")

threading.Thread(target=receive, daemon=True).start()

while True:
    text = input("Event/message (quit to stop): ")
    if text.lower() == "quit":
        break
    with lock:
        vector.setdefault(name, 0)
        vector[name] += 1
        values = ",".join(f"{p}:{vector[p]}" for p in sorted(vector))
        current = dict(vector)
    client.sendall(f"EVENT|{name}|{values}|{text}\n".encode())
    print("Sent with vector timestamp:", current)

client.close()
