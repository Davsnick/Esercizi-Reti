#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h> 

void error(char *msg){
    perror(msg);
    exit(0);
}

/*
	The BSD server creates a socket, uses bind to attach that socket to a port,
	and configures it as a listening socket.
	This allows the server to receive incoming connection requests.
	Afterwards, accept is called, which will block the socket,
	until an incoming connection request is received
*/
int main(int argc, char *argv[]){
    int sockfd, portno, n;
	char buffer[256];
	/* sockaddr_in: IPv4 Socket Address structure */
    struct sockaddr_in serv_addr;
    struct hostent *server;

	// control arguments
    if (argc < 3) {
       fprintf(stderr,"usage %s hostname port\n", argv[0]);
       exit(0);
    }
    portno = atoi(argv[2]);

	/*
		SOCKET
		Creates a communication socket
		AF_INET means using IPv4
		SOCK_STREAM means using TCP
		use SOCK_DGRAM for UDP
		INADDR_ANY means all IP addresses accepted

		int socket(family, type, protocol)
	*/
    if (sockfd = socket(AF_INET, SOCK_STREAM, 0) < 0)
		error("ERROR opening socket");

    if (server = gethostbyname(argv[1]) == NULL) {
        fprintf(stderr,"ERROR, no such host\n");
        exit(0);
    }
    bzero((char *) &serv_addr, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    bcopy((char *)server->h_addr, (char *)&serv_addr.sin_addr.s_addr, server->h_length);
    serv_addr.sin_port = htons(portno);
    if (connect(sockfd,(const struct sockaddr *) &serv_addr,sizeof(serv_addr)) < 0) 
        error("ERROR connecting");

    printf("Please enter the message: ");
    bzero(buffer, 256);
    fgets(buffer, 255, stdin);

    if (write(sockfd, buffer, strlen(buffer)) < 0)
         error("ERROR writing to socket");


    bzero(buffer,256);
    if (n = read(sockfd, buffer, 255) < 0)
         error("ERROR reading from socket");
    printf("%s\n",buffer);
    return 0;
}
