//
// Created by 吴化吉 on 2019-08-05.
//
/*请求包*/
typedef struct {
    /*请求行*/
    struct request_line{
        char *method;
        char *uri;
        char *protocol;
    } req_line;

    /*请求头字段*/
    struct request_header{
        char *host;
        char *connection;
        char *useragent;
        char *accept;
        char *acceptencoding;
        /* 先读取基本字段，更多的的之后再读 */
    } req_header;
} request_package;

/*响应包*/
typedef struct {
    /*响应状态*/
    char *res_status;
//    struct response_status{
//        char *protocol;
//        char *status_code;
//        char *status_text;
//    } res_status;

    /*响应头*/
    struct response_header{
        char *server;
        char *contenttype;
        /* 更多的字段之后再补充 */
    } res_header;

    char *body ;
} response_package;


request_package parse_request(int client);
int send_response(int client_fd,request_package req_package);