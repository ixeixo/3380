// Ethan Riley, 2022.
//
// Pcap sniffer, used as part of a group project in CSC3380
//
// Based on:
//
/*
  PROGRAMMING WITH PCAP
  Copyright (C) 2002	Tim Carstens <timcarst@yahoo.com>
  Copyright (C)	2002	Guy Harris <guy@alum.mit.edu>
*/

// Compile with:
//
//   gcc -Wall -o sniffer sniffer.c -lpcap
//

#include <pcap.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

//ethernet headers are exactly 14 bytes
#define SIZE_ETHERNET 14

/* Ethernet addresses are 6 bytes */
#define ETHER_ADDR_LEN	6


/* Ethernet header */
struct sniff_ethernet {
	u_char ether_dhost[ETHER_ADDR_LEN]; 
	/* Destination host address */

	u_char ether_shost[ETHER_ADDR_LEN]; 
	/* Source host address */

	u_short ether_type; 
	/* IP? ARP? RARP? etc */

};


/* IP header */
struct sniff_ip {
	u_char ip_vhl;		
	/* version << 4 | header length >> 2 */

	u_char ip_tos;
	/* type of service */

	u_short ip_len;	
	/* total length */

	u_short ip_id;	
	/* identification */

	u_short ip_off;	
	/* fragment offset field */

	#define IP_RF 0x8000
	/* reserved fragment flag */

	#define IP_DF 0x4000
	/* don't fragment flag */

	#define IP_MF 0x2000
	/* more fragments flag */

	#define IP_OFFMASK 0x1fff
	/* mask for fragmenting bits */

	u_char ip_ttl;	
	/* time to live */

	u_char ip_p;
	/* protocol */

	u_short ip_sum;	
	/* checksum */

	struct in_addr ip_src,ip_dst;
       	/* source and dest address */

};

#define IP_HL(ip)		(((ip)->ip_vhl) & 0x0f)
#define IP_V(ip)		(((ip)->ip_vhl) >> 4)


/* TCP header */
typedef u_int tcp_seq;

struct sniff_tcp {
	u_short th_sport;	
	/* source port */

	u_short th_dport;
	/* destination port */

	tcp_seq th_seq;	
	/* sequence number */

	tcp_seq th_ack;	
	/* acknowledgement number */

	u_char th_offx2;
	/* data offset, rsvd */

	#define TH_OFF(th)	(((th)->th_offx2 & 0xf0) > 4)
	u_char th_flags;

	#define TH_FIN 0x01

	#define TH_SYN 0x02

	#define TH_RST 0x04

	#define TH_PUSH 0x08

	#define TH_ACK 0x10

	#define TH_URG 0x20

	#define TH_ECE 0x40

	#define TH_CWR 0x80

	#define TH_FLAGS (TH_FIN|TH_SYN|TH_RST|TH_ACK|TH_URG|TH_ECE|TH_CWR)
	
	u_short th_win;
	/* window */

	u_short th_sum;	
	/* checksum */

	u_short th_urp;	
	/* urgent pointer */

};

void got_packet(u_char *args, const struct pcap_pkthdr *header, const u_char *packet)
{

	const struct sniff_ethernet *ethernet; 
	/* The ethernet header */

	const struct sniff_ip *ip; 
	/* The IP header */

	const struct sniff_tcp *tcp; 
	/* The TCP header */

	const char *payload; 
	/* Packet payload */

	u_int size_ip;

	u_int size_tcp;

	ethernet = (struct sniff_ethernet*)(packet);
	ip = (struct sniff_ip*)(packet + SIZE_ETHERNET);
	size_ip = IP_HL(ip)*4;


	if (size_ip < 20) {

		printf("   * Invalid IP header length: %u bytes\n", size_ip);
		return;

	}


	tcp = (struct sniff_tcp*)(packet + SIZE_ETHERNET + size_ip);
	size_tcp = TH_OFF(tcp)*4;

	if (size_tcp < 20) {
		
		printf("   * Invalid TCP header length: %u bytes\n", size_tcp);
		return;

	}

	payload = (u_char *)(packet + SIZE_ETHERNET + size_ip + size_tcp);
}


int main(int argc, char *argv[])
{
	char errbuf[PCAP_ERRBUF_SIZE];
	//most libpcap commands allow errbuf to be passed as an arg
	//in case of failure errbuf will be loaded with an error message
	
	pcap_if_t *interfaces; 
	//libpcap defined structure; will hold device names
    	

	//___Identifying Device(s)___

    	if(pcap_findalldevs(&interfaces,errbuf)==-1)
    	//pcap_findalldevs() constructs a list of network devices that can be opened with 
	//pcap_create(3PCAP) and pcap_activate
	
	{
        	printf("\nFAIL:%s",errbuf);
        	return -1;   
		//If pcap_findalldevs() succeeds, the pointer pointed 
		//to by interfaces is set to point to the first element of the 
		//list, or to NULL if no devices were found
		
		//access first element of list of devices: interfaces->name 
    	}	

	pcap_t *handle;

	//____OPENING DEVICE____
	//****FIGURE OUT HOW TO KEEP GOING UNTIL JPEG EOF IS FOUND ETC******

	handle = pcap_open_live(interfaces->name, BUFSIZ, 1, 1000, errbuf);
	//pcap_open_live(): used to obtain a packet capture handle to look at packets on network
	//devce name, shapshot length, promiscuous mode off == 0 else ON, timeout in milliseconds
	//returns pcap_t (handle in this case) on success, NULL on failure


	if (handle == NULL) {
		fprintf(stderr, "Couldn't open device %s: %s\n", interfaces->name, errbuf);
		return(2);
	}


	if (pcap_datalink(handle) != DLT_EN10MB) {
	//returns the link-layer header type for the live capture or ``savefile''  
	//DLT_EN10MB for Ethernet
	//Following presumes Eithernet Headers.
		fprintf(stderr, "Device %s doesn't provide Ethernet headers - not supported\n", interfaces->name);
		return(2);
	}



	//____Traffic Filtering____
	
	//This preps the sniffer to sniff all traffic coming from or going to port 23, (******PORT CHANGE?******)
	//with promiscuous ON, on the device ETH0.
	
	struct bpf_program fp;		//The compiled filter expression 
	char filter_exp[] = "port 23";	/* The filter expression */
	bpf_u_int32 mask;		/* The netmask of our sniffing device */
	bpf_u_int32 net;		/* The IP of our sniffing device */


	if (pcap_lookupnet(interfaces->name, &net, &mask, errbuf) == -1) {
	//used to determine the IPv4 network number and mask associated with the network device device. 
	//Both netp and maskp are bpf_u_int32 pointers. 
		fprintf(stderr, "Can't get netmask for device %s\n", interfaces->name);
		net = 0;
		mask = 0;
	}


	if (pcap_compile(handle, &fp, filter_exp, 0, net) == -1) { //Before applying filter "compile" it. 
	//used to compile a string into a filter program. 
	//The resulting filter program can then be applied to 
	//some stream of packets to determine which packets will be supplied
	//to pcap_loop(_dispatch)(next)(next_ex)
 
		fprintf(stderr, "Couldn't parse filter %s: %s\n", filter_exp, pcap_geterr(handle));
		return(2);
	}


	if (pcap_setfilter(handle, &fp) == -1) { //After "compiling" our filter, time to apply it

		fprintf(stderr, "Couldn't install filter %s: %s\n", filter_exp, pcap_geterr(handle));
		return(2);
	}


	//____SNIFFING____
	
	/* now we can set our callback function */
        pcap_loop(handle, BUFSIZ, got_packet, NULL);

	/* cleanup */
        pcap_freecode(&fp);
        pcap_close(handle);
}
