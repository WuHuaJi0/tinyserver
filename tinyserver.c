#include <netinet/in.h>
#include "src/header/tcp.h"
#include <stdio.h>
#include <unistd.h>
#include "src/header/http.h"
#include <time.h>


int main() {
    /*创建一个tcp端口并监听*/
    int listenfd;
    struct sockaddr_in clientaddr;
    socklen_t clientaddrlen;

    long timestramp = time(NULL);
    int port = timestramp % 3000 + 1000;

    listenfd = open_listenfd(port);
    printf("监听在 %d 端口上\n", port);

    if (listenfd == -1) {
        return -1;
    }

    while (1) {
        int client_fd = accept(listenfd, (struct sockaddr *) &clientaddr, &clientaddrlen);
        if (client_fd == -1) {
            perror("accept");
            break;
        }
        request_package req_package = parse_request(client_fd);
        send_response(client_fd,req_package);
        close(client_fd);
    }
}