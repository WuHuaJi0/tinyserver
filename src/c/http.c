/** 
 * Created by 吴化吉
 **/
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include "../header/http.h"

/* TODO: 如果 buf_size 个字节 不够存怎么办？*/
#define BUF_SIZE 200


int readline(int client_fd, char *line){
    char c ;
    int index = 0;

    bzero(line, BUF_SIZE);

    /* 逐个读取一个字符 */
    while (read(client_fd,&c,1) > 0){
        line[index] = c;
        index ++;
        if( c == '\n'){
            return index;
        }
    }
    return index;
}


/* 解析请求行 method ,url, protocol , eg : GET /index.html HTTP/1.1 */
int parse_request_line(char *line, request_package *req_package){

    char *item = strtok(line," ");

    char *method = malloc(sizeof(char) * strlen(item));
    strcpy(method,item);
    req_package->req_line.method = method;

    item = strtok(NULL," ");
    char *uri = malloc(sizeof(char) * strlen(item));
    strcpy(uri,item);
    req_package->req_line.uri = uri;

    item = strtok(NULL," ");
    char *protocol = malloc(sizeof(char) * strlen(item));
    strcpy(protocol,item);
    req_package->req_line.protocol = protocol;
}


/* 解析其他请求字段 */
int parse_request_header(char *line, request_package *req_package){
    char *item = strtok_r(line,"\r\n",&line);
    while (item != NULL){
        printf("line: %s \n",item);
        char *key = strtok_r(item,": ",&item);
        char *value = strtok_r(NULL,": ",&item);
        printf("key: %s,value: %s\n",key,value);

        if( strcmp(key,"Host") == 0 ){
            req_package->req_header.host = strdup(value);
        }else if( strcmp(key,"Connection") == 0 ){
            req_package->req_header.connection = strdup(value);
        }else if( strcmp(key,"Connection") == 0 ){
            req_package->req_header.connection = strdup(value);
        }else if( strcmp(key,"User-Agent") == 0 ){
            req_package->req_header.useragent = strdup(value);
        }else if( strcmp(key,"Accept") == 0 ){
            req_package->req_header.accept = strdup(value);
        }else if( strcmp(key,"Accept-Encoding") == 0 ){
            req_package->req_header.acceptencoding = strdup(value);
        }
        item = strtok_r(NULL,"\r\n",&line);
    }
    return 0;
}


/* 解析HTTP报文 */
int parse_request(client_fd){

    char line[BUF_SIZE];
    request_package req_package;

    int index_line = 0;
    while ( readline(client_fd,line) > 0 ){
        if( strcmp(line,"\r\n") ){ /* strcmp根据ascii码来比较，不是\r\n 都会为true */
            /*第一行是请求行*/
            if( index_line == 0 ){
                parse_request_line(line,&req_package);
                index_line++;
                continue;
            }

            parse_request_header(line,&req_package);

        }else{
            break;
        }
    }
    return 0;
}