#pragma once
#include <netinet/ip.h>

typedef struct {
    int len;
    int num;
} msgdata;

typedef struct {
    // ether_header    ethernetHeader;
    struct ip          ipHeader;
    // tcphdr          tcpHeader;
    msgdata            data;
} msgstruct;

#define D_OK    0
#define D_ERR   -1

#define INET_ADDRSTRLEN 40

#define D_DST_IP       0xC0A80101      // 192.168.1.1 (https://www.browserling.com/tools/ip-to-hex)
// #define D_PORT      60029
