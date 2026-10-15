import socket
# Imports Python's socket module so you can create network connections.
# Required for making both servers and clients.

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Creates a new TCP socket.
# AF_INET  → IPv4
# SOCK_STREAM → TCP (reliable, connection‑based protocol)

sock.connect(('localhost', 5555))
# Connects to a server running on the same machine ("localhost")
# on port 5555.
# This must match the server's bind() address and port.

 while True:
    # Infinite loop so the client keeps sending data forever.

    sock.send('Hello, world'.encode('utf-8'))
    # Sends the string "Hello, world" to the server.
    # encode('utf-8') converts the text into bytes,
    # because sockets can only send raw bytes.
