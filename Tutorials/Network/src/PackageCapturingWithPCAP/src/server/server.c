#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <errno.h>

#include <sys/socket.h>
#include <sys/syscall.h>
#include <arpa/inet.h>

#include "if.h"

int setIpHeader(unsigned int dst, unsigned int len, void* data_p)
{
    struct ip* header = (struct ip*)data_p;
    int selfIp = (int)syscall(SYS_gettid);
    header->ip_v          = 4;				// ipV4
    header->ip_hl         = sizeof(*header)/4;
    header->ip_tos        = 0;
    header->ip_len        = htons(len);
    header->ip_id         = 0;				// freeID
    header->ip_off        = 0;				// don't flagment
    header->ip_ttl        = 255;
    header->ip_p          = IPPROTO_RAW;
    header->ip_sum        = 0;
    header->ip_src.s_addr = htonl(selfIp);
    header->ip_dst.s_addr = dst;
    return (sizeof(*header));
}

void printPackage_hex(const void* data_p, int len)
{
    int linecnt = 16;
    const unsigned char* buf = (unsigned char*)data_p;
    for (int i = 0; i < len; i += linecnt) {
        putc('\n', stdout);
        for (int j = 0; j < linecnt; j++) {
            putc(' ', stdout);
            const char HEX[] = {'0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F'};
            putc(i+j<len ? HEX[buf[i+j] >> 4] : ' ', stdout);
            putc(i+j<len ? HEX[buf[i+j] & 0x0F] : ' ', stdout);
        }
        putc('|', stdout);
        putc(' ', stdout);
        for (int j = 0; j < linecnt; j++) {
            putc(i+j < len ? (buf[i+j] >= ' ' && buf[i+j] <= 'z' ? buf[i+j] : '.') : ' ', stdout);
        }
    }
}

int createSocket(unsigned int ipaddr_ofs, struct sockaddr_in* socket_in, int& socketHandler)
{
    int onoff = 1;

    // Create a new socket
    if ( (socketHandler = socket(PF_INET, SOCK_RAW, IPPROTO_RAW)) == -1 ) {     //  IPPROTO_TCP
        printf("\n[ERROR] [%s:%d] Failed to init socket", __FILE__, __LINE__);
        printf("\nError code: %d. Error log: %s", errno, strerror(errno));
        return D_ERR;
    }
    if ( (setsockopt(socketHandler, IPPROTO_IP, IP_HDRINCL, &onoff, sizeof(int))) == -1 ) {    // IPPROTO_TCP
        printf("\n[ERROR] [%s:%d] Failed to set socket options", __FILE__, __LINE__);
        printf("\nError code: %d. Error log: %s", errno, strerror(errno));

        close(socketHandler);
        return D_ERR;
    }

    // Set socket info
    socket_in->sin_family      = PF_INET;
    socket_in->sin_addr.s_addr = htonl(ipaddr_ofs);
    // sin.sin_addr.s_addr     = inet_addr(D_IP);
    // socket_in->sin_port     = htons(D_PORT);

    /////////////////////////
    // DEBUG
    char ipStr[40];
    printf("\n[INFO] Destination address: %s", inet_ntop(PF_INET, &(socket_in->sin_addr), ipStr, sizeof(ipStr)));
    printf("\n[INFO] Port: %d", ntohs(socket_in->sin_port));
    /////////////////////////

    return D_OK;
}

int sendPackage(int app, msgstruct* data_p, struct sockaddr_in* socket_in, int socketHandler)
{
    unsigned int        datalen = 0;

    if (data_p == NULL) {
        printf("\n[ERROR] [%s:%d] NULL data", __FILE__, __LINE__);
        return D_ERR;
    }

    if ( (unsigned int)data_p->data.len > sizeof(msgstruct) ) {	
        printf("\n[ERROR] [%s:%d] Invalid size of data (sent msg size: %d > struct size: %lu)", __FILE__, __LINE__, data_p->data.len, sizeof(msgstruct));
        return D_ERR;
    }

    // Set header for IP
    datalen += data_p->data.len;
    datalen += setIpHeader(socket_in->sin_addr.s_addr, datalen, data_p);

    // Bind socket to port. Note: Only possible when host is local (not remote)
    // if( bind(socketHandler, (sockaddr*)socket_in, sizeof(socket_in)) == -1)
    // {
    //     printf("\n[ERROR] [%s:%d] Failed to bind socket t, __FILE__, __LINE__);
    //     printf("\nError code: %d. Error log: %s", errno, strerror(errno));
    //     return D_ERR;
    // }

    printPackage_hex((u_char*)data_p, datalen);

    ssize_t sndByteNum = sendto(socketHandler, data_p, datalen, 0, (struct sockaddr*)socket_in, sizeof(struct sockaddr_in));
    if (sndByteNum == -1) {
        printf("\n[ERROR] [%s:%d] Failed to send message.", __FILE__, __LINE__);
        printf("\nError code: %d. Error log: %s", errno, strerror(errno));
        return D_ERR;
    }
    printf("\n[INFO] Sent %lu (bytes)", sndByteNum);

    return D_OK;
}

int main()
{
    msgstruct msgSnd;
    msgSnd.data.len = sizeof(msgstruct);
    msgSnd.data.num = 1;

    struct sockaddr_in socket_in;
    memset(&socket_in, 0, sizeof(struct sockaddr_in));
    int socketHandler;
    
    if (createSocket(D_DST_IP, &socket_in, socketHandler) == D_ERR) {
        return D_ERR;
    }

    while (true) {
        if ( sendPackage(0, &msgSnd, &socket_in, socketHandler) == D_ERR ) {
            printf("\n[ERROR] [%s:%d] Failed to send message", __FILE__, __LINE__);
            return D_ERR;
        }
        sleep(2);
        printf("\n");
    }

    close(socketHandler);

    return D_OK;
}
