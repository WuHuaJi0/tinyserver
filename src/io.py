# 将select库导成 s，避免和select方法冲突
import select as s
from . import http


def select(server):
    print("使用 select ")
    fd = [server]
    while True:
        result = s.select(fd, [], [], 0)
        for sock in result[0]:
            if sock == server:
                (client, address) = server.accept()
                fd.append(client)
            else:
                request = http.get_request(sock)
                if not request:
                    sock.close()
                    del fd[fd.index(sock)]
                    continue

                http.send_response(sock, request)

                if not http.is_keep_alive(request):
                    sock.close()
                    del fd[fd.index(sock)]


def poll(server):
    print("使用poll")
    poll = s.poll()
    poll.register(server, s.POLLIN)

    all_clients = {}
    while True:
        result = poll.poll(1000)
        for (fd, event) in result:
            if fd == server.fileno():
                (client, address) = server.accept()
                poll.register(client, s.POLLIN)
                all_clients[client.fileno()] = client
            else:
                client = all_clients[fd]
                request = http.get_request(client)
                if not request:
                    client.close()
                    poll.unregister(fd)
                    del all_clients[fd]
                    continue

                http.send_response(client, request)

                if not http.is_keep_alive(request):
                    client.close()
                    poll.unregister(fd)
                    del all_clients[fd]


def epoll(server):
    print("使用epoll")
    epoll = s.epoll(1024)
    epoll.register(server, s.EPOLLIN)
    all_client = {}
    while True:
        all_fd = epoll.poll(1)
        for (fd, event) in all_fd:
            if fd == server.fileno():
                (client, address) = server.accept()
                all_client[client.fileno()] = client
                epoll.register(client, s.EPOLLIN)
            else:
                client = all_client[fd]
                request = http.get_request(client)
                if not request:
                    client.close()
                    epoll.unregister(fd)
                    del all_client[fd]
                    continue
                http.send_response(client, request)

                if not http.is_keep_alive(request):
                    client.close()
                    epoll.unregister(fd)
                    del all_client[fd]