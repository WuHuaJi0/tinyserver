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

    port_file = open("./tinyserver.port","w")
    port_file.write(str(port))
    port_file.close()

    server = tcp.listen(port)

    mode = select_mode()
    selector = io.IO(mode)
    selector.wait(server)


if __name__ == '__main__':
    main()
