import socket

# create a server socket , and bind to a port , then listen client connect.
def server_listen(port=3000):
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)
    server_socket.bind(("", port))
    server_socket.listen(100)
    return server_socket