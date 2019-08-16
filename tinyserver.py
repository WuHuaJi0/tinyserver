from src import tcp
from src import io
import random
import sys


# 选择io复用模型
def select_mode():
    types = ["select", "poll", "epoll"]
    for i in sys.argv:
        args = i.split("=")
        if len(args) == 2 and args[0] == 'mode' and args[1] in types:
            return args[1]
    return "select"


def main():
    port = random.randint(1000, 3000)

    print("监听在：" + str(port) + " 端口")
    server = tcp.server_listen(port)

    mode = select_mode()
    if mode == 'select':
        io.select(server)
    elif mode == "poll":
        io.poll(server)
    elif mode == "epoll":
        io.epoll(server)


if __name__ == '__main__':
    main()
