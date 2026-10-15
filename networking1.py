import socket
# Imports Python's socket library so you can create network connections.
# Without this, you cannot make servers or clients.

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Creates a new TCP socket.
# AF_INET  → use IPv4 addresses
# SOCK_STREAM → use TCP (reliable, connection‑based)

sock.bind(('0.0.0.0', 5555))
# Binds the socket to IP 0.0.0.0 and port 5555.
# 0.0.0.0 means "listen on ALL network interfaces" (LAN, WiFi, etc.)
# This is the port clients must connect to.

sock.listen()
# Puts the socket into listening mode.
# This tells the OS: "I am a server, waiting for incoming connections."

while True:
    # Infinite loop so the server never stops.
    # It keeps accepting new clients forever.

    connection, address = sock.accept()
    # Waits until a client connects.
    # When a client connects:
    #   connection → a new socket just for that client
    #   address → the client's IP and port

    print("connection from: ", address)
    # Prints the client's address so you can see who connected.

    data = connection.recv(1024)
    # Receives up to 1024 bytes of data from the client.
    # This pauses until the client actually sends something.

    message = data.decode('utf-8')
    # Converts the raw bytes into a readable string using UTF‑8 encoding.

    print(message)
    # Prints the message the client sent.
