# http 性能测试
import os
import random
from http import client
import time
from multiprocessing import Pool


CONNECTION_NUM = 1000 #connection 数量
PROCESS_NUM = 40
REQUEST_NUM = 10000 #请求数量

def rand_connection():
    rand = random.randint(0, CONNECTION_NUM)
    while(rand in using_connection):
        rand = random.randint(0, CONNECTION_NUM)
    return rand
    

def request(i):
    rand = rand_connection()
    using_connection.add(rand)
    connection = connections[rand]
    print("发送第" + str(i) + "个请求,进程号是" + str(os.getpid()))
    connection.request('GET', '/', None, {"Connection": "keep-alive"})
    response = connection.getresponse()
    print(response.read(1000).decode('UTF-8'))
    using_connection.remove(rand)

# 初始化 HTTPConnection
connections = []
using_connection = {-1,}
for i in range(CONNECTION_NUM):
    port_file = open("./tinyserver.port","r")
    port = port_file.read(4)
    connection = client.HTTPConnection("localhost", port)
    connections.append(connection)



before = time.time()
po = Pool(PROCESS_NUM)
for i in range(REQUEST_NUM):
    po.apply_async(request, (i,))

po.close()
po.join()

after = time.time()
print("消耗的时间", after - before)
