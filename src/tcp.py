import socket

# create a server socket , and bind to a port , then listen client connect.
def listen(port=3000):
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)
    server.bind(("", port))
    server.listen(100)
    return server