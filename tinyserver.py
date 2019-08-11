import os

from src import tcp
from src import http
import random

if __name__ == '__main__':
    port = random.randint(1000, 3000)

    print("监听在：" + str(port) + " 端口")
    server_socket = tcp.server_listen(port)
    while True:
        (client_socket, address) = server_socket.accept()

        # 使用子进程来处理请求
        if os.fork() == 0:
            while True:
                request_string = client_socket.recv(1000)
                if not request_string:
                    continue
                request = http.parse_request(request_string)
                http.send_response(client_socket, request)
                # client_socket.close()
        else:
            continue
