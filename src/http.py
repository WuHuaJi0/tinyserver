import os


def get_request(client_sock):
    request = {
        # 请求行
        "request_line": {
            "method": "",
            "uri": "",
            "protocol": "",
        },
        # 请求头
        "header": {},
        "body": ""
    }
    index_line = 1
    line = ""
    while True:
        char = client_sock.recv(1)
        # 据recv文档，如果 request_string 为空，则客户端已经关闭连接了：
        if not char:
            return False

        line += char.decode("UTF-8")

        # 如果是空行，则接下来就是请求体，如果有 Content-length,则有请求体;如果没有Content-length，则请求报文已经读完
        if line == "\r\n":
            if "Content-Length" in request["header"]:
                request["body"] = client_sock.recv[request["header"]["Content-Length"]]
            return request

        # 如果是读取到了行末，就解析此行数据
        if line[-2:] == "\r\n":
            if index_line == 1:
                (request['request_line']['method'], request['request_line']['uri'],
                 request['request_line']['protocol']) = parse_request_line(line[0:-2])
            else:
                key_value = parse_request_header(line[0:-2])
                request["header"][key_value[0]] = key_value[1]
            line = ""
            index_line += 1


def parse_request_line(string):
    method_url_protocol = string.split(" ")
    if method_url_protocol[1] == '/':
        method_url_protocol[1] = "/index.html"
    return method_url_protocol


def parse_request_header(request_line):
    return request_line.split(": ")


# 返回静态文件
def send_response(client_socket, request_package):
    response = {
        "status": "HTTP/1.1 200 OK",
        "response_header": {
            "Server": "Tinyserver by wuhuaji",
            # "Connection": "keep-alive",
            "Content-Length": "",
        },
        "body": ""
    }

    file_path = "./static" + request_package['request_line']['uri']

    if not os.access(file_path, os.F_OK):
        file = open("./static/error/404.html")
    elif not os.access(file_path, os.R_OK):
        file = open("./static/error/403.html")
    else:
        file = open(file_path)

    response['body'] = file.read()
    response["response_header"]["Content-Length"] = str(len(response['body']))
    file.close()

    response_string = response['status'] + "\r\n"
    for i in response["response_header"]:
        response_string += i + ": " + response["response_header"][i] + "\r\n"
    response_string += "\r\n"

    response_string += response["body"]
    client_socket.send(response_string.encode("UTF-8"))