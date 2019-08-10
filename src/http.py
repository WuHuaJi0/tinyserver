import os
from os.path import realpath


def parse_request_line(string):
    method_url_protocol = string.split(" ")
    if method_url_protocol[1] == '/':
        method_url_protocol[1] = "/index.html"
    return method_url_protocol


def parse_request_header(request_line):
    request_header = {}
    for i in range(1, len(request_line)):
        key_value = request_line[i].split(": ")
        if len(key_value) == 2:
            request_header[key_value[0]] = key_value[1]
    return request_header


# 解析请求包的内容
def parse_request(request_string):
    request = {
        # 请求行
        "request_line": {
            "method": "",
            "uri": "",
            "protocol": "",
        },
        # 请求头
        "header": {}
    }

    request_lines = request_string.decode("UTF-8").split("\r\n")

    (request['request_line']['method'], request['request_line']['uri'],
     request['request_line']['protocol']) = parse_request_line(request_lines[0])

    request['header'] = parse_request_header(request_lines)

    return request


# 返回静态文件
def send_response(client_socket,request_package):
    response = {
        "status": "HTTP/1.1 200 OK",
        "response_header": {
            "Server": "Tinyserver by wuhuaji",
        },
        "body": ""
    }

    file_path = "./static" + request_package['request_line']['uri']

    print(os.path.dirname(__file__))

    print(realpath(file_path))

    if not os.access(file_path, os.F_OK):
        file = open("./static/error/404.html")
    elif not os.access(file_path, os.R_OK):
        file = open("./static/error/403.html")
    else:
        file = open(file_path)

    response['body'] = file.read()
    file.close()

    response_string = response['status'] + "\r\n"
    for i in response["response_header"]:
        response_string += i + ": " + response["response_header"][i] + "\r\n\r\n"

    response_string += response["body"]
    client_socket.send(response_string.encode("UTF-8"))

