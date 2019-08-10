from src import tcp
from src import http
import random

if __name__ == '__main__':
    port = random.randint(1000,3000)

    print("监听在："+ str(port) +" 端口")
    server_socket = tcp.server_listen(port)
    while True:
        server_socket.accept()
        (client_socket, address) = server_socket.accept()

        # todo: 这里假定1000个字符把http请求头读取完了，实际上可能没有；
        request_string = client_socket.recv(1000)
        request = http.parse_request(request_string)
        http.send_response(client_socket,request)
        client_socket.close()