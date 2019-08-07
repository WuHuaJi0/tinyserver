//
// Created by 吴化吉 on 2019-08-05.
//
/*请求包*/
typedef struct {
    struct request_line{
        char *method;
        char *uri;
        char *protocol;
    } req_line;

    struct request_header{
        char *host;
        char *connection;
        char *useragent;
        char *accept;
        char *acceptencoding;
        /* 先读取基本字段，更多的的之后再读 */
    } req_header;
} request_package;



int parse_request(int client);
int send_response(int client_fd);