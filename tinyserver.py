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
                # recv 是个阻塞函数，没有数据流入会阻塞在此处
                request_string = client_socket.recv(1000)

                # 据recv文档，如果 request_string 为空，则客户端已经关闭连接了：
                if not request_string:
                    exit(0)

                request = http.parse_request(request_string)
                http.send_response(client_socket, request)


        else:
            continue
