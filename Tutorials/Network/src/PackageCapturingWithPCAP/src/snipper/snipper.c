#include <pcap.h>
#include <stdio.h>
#include <errno.h>

#include <netinet/in.h>
#include <netinet/ip.h>
#include <netinet/if_ether.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netinet/tcp.h>

#include "if.h"

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

void packetHandler(u_char *userData, const struct pcap_pkthdr* pkthdr, const u_char* packet)
{
    ip*             ipHeader;

    ipHeader = (ip*)(packet + sizeof(ether_header));
    char srcIp_str[INET_ADDRSTRLEN];
    char dstIp_str[INET_ADDRSTRLEN];
    inet_ntop(PF_INET, &(ipHeader->ip_src), srcIp_str, sizeof(srcIp_str));
    inet_ntop(PF_INET, &(ipHeader->ip_dst), dstIp_str, sizeof(dstIp_str));

    // DEBUG
    /////////////////////////
    msgdata* body = (msgdata*)(packet + sizeof(ether_header) + sizeof(ip));
    printf("\nFull package length: %d", pkthdr->len);
    printf("\nSource IP: %s. Destination IP: %s", srcIp_str, dstIp_str);
    printf("\nBody infor: Length = %d, num = %d\n", body->len, body->num);
    ///////////////////////
}

int main(int argc, char *argv[])
{
    pcap_t *handle;                         /* Session handle */
    char *dev;                              /* The device to sniff on */
    char errbuf[PCAP_ERRBUF_SIZE];          /* Error string */
    struct bpf_program fp;                  /* The compiled filter */
    char filterExp[128];	                /* The filter expression */
    bpf_u_int32 mask;                       /* Our netmask */
    bpf_u_int32 net;                        /* Our IP */

    /* Convert IP number to IP human-ready string */
    struct in_addr ip_addr;
    char ipStr[INET_ADDRSTRLEN];
    ip_addr.s_addr = htonl(D_DST_IP);
    strncpy(ipStr, inet_ntoa(ip_addr), sizeof(ipStr));

    /* Create filter expression */
    snprintf(filterExp, sizeof(filterExp), "dst %s", ipStr);
    printf("\n[INFO] [%s:%d] Filter expression: %s", __FILE__, __LINE__, filterExp);

    /* Define the network interface */
    dev = pcap_lookupdev(errbuf);
    if (dev == NULL) {
        printf("\n[ERROR] [%s:%d] Failed to find default network interface.", __FILE__, __LINE__);
        printf("\nError log: %s", errbuf);
        return D_ERR;
    }
    printf("\n[INFO] [%s:%d] Define the network interface: %s", __FILE__, __LINE__, dev);

    /* Find the properties for the network interface */
    if (pcap_lookupnet(dev, &net, &mask, errbuf) == -1) {
        printf("\n[ERROR] [%s:%d] Failed to get netmask for network interface %s", __FILE__, __LINE__, dev);
        printf("\nError log: %s", errbuf);
        net = 0;
        mask = 0;
        return D_ERR;
    }
    printf("\n[INFO] [%s:%d] Find the properties for the network interface (net: %d, mask: %d)", __FILE__, __LINE__, net, mask);

    /* Open the session in promiscuous mode */
    handle = pcap_open_live(dev, BUFSIZ, 1, 1000, errbuf);
    if (handle == NULL) {
        printf("\n[ERROR] [%s:%d] Failed to open pcap live session %s", __FILE__, __LINE__, dev);
        printf("\nError log: %s", errbuf);
        return D_ERR;
    }

    /* Compile and apply the filter */
    if (pcap_compile(handle, &fp, filterExp, 0, net) == -1) {
        printf("\n[ERROR] [%s:%d] Failed to parse filter %s. Error: %s", __FILE__, __LINE__, filterExp, pcap_geterr(handle));
        return D_ERR;
    }
    if (pcap_setfilter(handle, &fp) == -1) {
        printf("\n[ERROR] [%s:%d] Failed to install filter %s. Error: %s",  __FILE__, __LINE__, filterExp, pcap_geterr(handle));
        return D_ERR;
    }

    /* Infinite loop which captures packages */
    pcap_loop(handle, -1, packetHandler, NULL);

    /* Close the pcap session */
    pcap_close(handle);

    return D_OK;
}
