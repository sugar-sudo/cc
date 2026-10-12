# Question: Task 1 - Create a simple socket connection where the client sends a message
# and the server responds. Send numbers to the server and display the sum.

import socket

HOST = "127.0.0.1"
PORT = 5001

numbers = input("Enter numbers separated by spaces: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
client.sendall(numbers.encode())

response = client.recv(4096).decode()
print("Server:", response)
client.close()
