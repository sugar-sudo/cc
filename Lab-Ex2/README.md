# Exercise 02 - Remote Method Invocation (RMI)

The PDF asks for a Calculator service with `add_numbers` and `multiply`, exposed through Pyro4, registered with a daemon, and invoked by a client using the generated URI. fileciteturn0file1L10-L25

Install:

```bash
pip install Pyro4
```

Run:

```text
python server.py
python client.py
```

Copy the URI printed by the server into the client.
