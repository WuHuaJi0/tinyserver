#include <netinet/in.h>
#include "src/header/tcp.h"
#include <stdio.h>
#include <unistd.h>
#define BUF_SIZE 100

int main() {
    /*创建一个tcp端口并监听*/
    int listenfd;
    struct sockaddr_in clientaddr;
    socklen_t clientaddrlen;
    listenfd = open_listenfd(3000);
    if( listenfd == -1 ){
        return -1;
    }
    printf("listen %d",listenfd);

    while(1) {
        int client_fd = accept(listenfd, (struct sockaddr *) &clientaddr, &clientaddrlen);
        if (client_fd == -1) {
            perror("accept");
            break;
        }

        int numRead ;
        char buf[BUF_SIZE];

        while ((numRead = read(client_fd,buf,BUF_SIZE)) > 0){
            if( write(STDOUT_FILENO,buf,numRead) != numRead ){
                perror("write"); return 0;
            }
        }

    }
}