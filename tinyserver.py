from src import tcp
from src import http
import random
import select


if __name__ == '__main__':
    port = random.randint(1000, 3000)

    print("监听在：" + str(port) + " 端口")
    server_socket = tcp.server_listen(port)
    readfiles = [server_socket]

    poll = select.poll()
    poll.register(server_socket, select.POLLIN)

    clients = {}
    while True:
        result = poll.poll(1000)
        for (sock, event) in result:

            if sock == server_socket.fileno():
                (client_socket, address) = server_socket.accept()
                poll.register(client_socket, select.POLLIN)
                clients[client_socket.fileno()] = client_socket
            else:
                client_socket = clients[sock]
                request = http.get_request(client_socket)
                if not request:
                    client_socket.close()
                    poll.unregister(sock)
                    del clients[sock]
                    continue

                http.send_response(client_socket, request)

                if "Connection" not in request["header"] or request["header"]["Connection"] != "keep-alive":
                    client_socket.close()
                    poll.unregister(sock)
                    del clients[sock]
