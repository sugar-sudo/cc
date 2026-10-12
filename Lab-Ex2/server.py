# Question: Define a Calculator service with addition and multiplication, expose it
# using Pyro4, register it with a Pyro4.Daemon, and listen for client requests.

import Pyro4

@Pyro4.expose
class Calculator:
    def add_numbers(self, a, b):
        return a + b

    def multiply(self, a, b):
        return a * b


daemon = Pyro4.Daemon()
uri = daemon.register(Calculator())

print("Server URI:", uri)
print("Waiting for client requests...")
daemon.requestLoop()
