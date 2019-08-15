import os

from src import tcp
from src import http
import socket
import random
import select

if __name__ == '__main__':
    port = random.randint(1000, 3000)

    print("监听在：" + str(port) + " 端口")
    server_socket = tcp.server_listen(port)
    readfiles = [server_socket]

    while True:
        result = select.select(readfiles, [], [], 0)
        for sock in result[0]:
            if sock == server_socket:
                (client_socket, address) = server_socket.accept()
                readfiles.append(client_socket)
            else:
                request = http.get_request(sock)
                if not request:
                    sock.close()
                    del readfiles[readfiles.index(sock)]
                    continue

                http.send_response(sock, request)

                if "Connection" not in request["header"] or request["header"]["Connection"] != "keep-alive":
                    sock.close()
                    del readfiles[readfiles.index(sock)]
