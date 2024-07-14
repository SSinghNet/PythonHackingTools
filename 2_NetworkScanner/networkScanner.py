#!usr/bin/env python
import scapy.all as scapy

def scan(ip):
    arpRequest = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arpRequestBroadcast = broadcast/arpRequest
    
    answered = scapy.srp(arpRequestBroadcast, timeout=1, verbose=False)[0]
    
    print("IP\t\t\tMAC Address\n----------------------------------------------------")
    
    
    for i in answered:
        print(i[1].psrc + "\t\t" + i[1].hwsrc)
    
scan("192.168.42.2/24")