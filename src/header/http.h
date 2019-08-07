//
// Created by 吴化吉 on 2019-08-05.
//


/*http请求行*/
typedef struct {
    char *method;
    char *uri;
    char *protocol;
} request_line;

/*请求头*/
typedef struct {
    char *host;
    char *connection;
    char *useragent;
    char *accept;
    char *acceptencoding;
    /* 先读取基本字段，更多的的之后再读 */
} request_header;


/*请求包*/
typedef struct {
    request_line req_line;
    request_header req_header;
} request_package;


int parse_request(int client);
int send_response(int client_fd);