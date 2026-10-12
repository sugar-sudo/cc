# Question: Prompt for the server URI, connect using Pyro4.Proxy, invoke
# add_numbers and multiply, and display both results on the client side.

import Pyro4

uri = input("Enter server URI: ").strip()
proxy = Pyro4.Proxy(uri)

a = float(input("Enter first number: "))
b = float(input("Enter second number: "))

print("Addition:", proxy.add_numbers(a, b))
print("Multiplication:", proxy.multiply(a, b))
