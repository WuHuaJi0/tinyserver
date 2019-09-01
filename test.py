# http 性能测试
import os
import random
from http import client
import time
from multiprocessing import Pool


def rand_connection():
    rand = random.randint(0, 1000)
    while(rand in using_connection):
        rand = random.randint(0, 1000)
    return rand
    

def request(i):
    rand = rand_connection()
    using_connection.add(rand)
    connection = connections[rand]
    print("发送第" + str(i) + "个请求,进程号是" + str(os.getpid()))
    connection.request('GET', '/', None, {"Connection": "keep-alive"})
    response = connection.getresponse()
    print(response.read(1000).decode('UTF-8'))
    time.sleep(0.05)
    using_connection.remove(rand)
    pass


connections = []
using_connection = {-1,}
for i in range(1000):
    connection = client.HTTPConnection("172.16.200.128", 1516)
    connections.append(connection)

before = time.time()
po = Pool(40)
for i in range(10000):
    po.apply_async(request, (i,))

po.close()
po.join()

after = time.time()
print("消耗的时间", after - before)
