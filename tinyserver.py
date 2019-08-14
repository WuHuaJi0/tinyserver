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
                request = http.get_request(client_socket)
                if not request:
                    exit()
                http.send_response(client_socket, request)

                if "Connection" not in request["header"] or request["header"]["Connection"] != "keep-alive":
                    client_socket.close()
                    exit()
        else:
            client_socket.close()
            continue
