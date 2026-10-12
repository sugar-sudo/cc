# Question: Implement Ricart-Agrawala mutual exclusion.
# On REQUEST: increment the logical clock and send a timestamped request.
# On REQUEST reception: reply immediately if our request has lower priority; otherwise defer.
# Enter the CS after receiving REPLY from every other process, then send deferred replies.

import socket
import threading
import time

HOST = "127.0.0.1"
PORT = 5005
name = input("Process name: ").strip()
clock = 0
request_time = None
deferred = []
replies = set()
peers = set()
lock = threading.Lock()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
client.sendall(name.encode())


def send(msg):
    client.sendall((msg + "\n").encode())


def receive():
    global clock, peers, request_time
    while True:
        data = client.recv(4096).decode()
        if not data:
            break
        for msg in data.splitlines():
            if msg.startswith("PEERS|"):
                peers = set(filter(None, msg.split("|", 1)[1].split(","))) - {name}
            elif msg.startswith("REQUEST|"):
                _, sender, ts = msg.split("|")
                ts = int(ts)
                clock = max(clock, ts) + 1
                mine = request_time
                if mine is None or (ts, sender) < (mine, name):
                    send(f"REPLY|{name}|{sender}")
                else:
                    deferred.append(sender)
            elif msg.startswith("REPLY|"):
                _, sender, target = msg.split("|")
                if target == name:
                    replies.add(sender)

threading.Thread(target=receive, daemon=True).start()

input("Press Enter to request the critical section...")
clock += 1
request_time = clock
replies.clear()
send(f"REQUEST|{name}|{request_time}")

while len(replies) < len(peers):
    time.sleep(0.1)

print(name, "entered critical section")
time.sleep(3)
print(name, "leaving critical section")

request_time = None
for peer in deferred:
    send(f"REPLY|{name}|{peer}")
deferred.clear()
client.close()
