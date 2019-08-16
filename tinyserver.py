from src import tcp
from src import http
import random
import select

if __name__ == '__main__':
    port = random.randint(1000, 3000)

    print("监听在：" + str(port) + " 端口")
    server_socket = tcp.server_listen(port)

    epoll = select.epoll(1024)
    epoll.register(server_socket, select.EPOLLIN)

    all_client = {}
    while True:
        all_fd = epoll.poll(1)
        for (fd, event) in all_fd:
            if fd == server_socket.fileno():
                (client,address) = server_socket.accept()
                print(client)
                print(client.fileno())
                all_client[client.fileno()] = client
                epoll.register(client, select.EPOLLIN )
            else:
                client = all_client[fd]
                request = http.get_request(client)
                if not request:
                    client.close()
                    epoll.unregister(fd)
                    del all_client[fd]
                    continue
                http.send_response(client, request)

                if "Connection" not in request["header"] or request["header"]["Connection"] != "keep-alive":
                    client.close()
                    epoll.unregister(fd)
                    del all_client[fd]
