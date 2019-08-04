/** 
 * Created by 吴化吉
 **/

#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>


int open_listenfd(int port){
    int listenfd ;
    struct sockaddr_in serveraddr;

    if( (listenfd = socket(AF_INET,SOCK_STREAM,0)) < 0  ){
        perror("listen");
        return -1;
    }

    bzero((char *) &serveraddr, sizeof(serveraddr));
    serveraddr.sin_family = AF_INET;
    serveraddr.sin_addr.s_addr = htonl(INADDR_ANY);
    serveraddr.sin_port = htons(port);
    if( bind(listenfd, (struct sockaddr *)&serveraddr, sizeof(serveraddr)) < 0 ){
        perror("bind");
        return -1;
    }
    
    if( listen(listenfd,1024)  < 0 ){
        perror("listen");
        return -1;
    }

    return listenfd;
}