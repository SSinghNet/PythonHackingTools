#!usr/bin/env python
import scapy.all as scapy

def scan(ip):
    arpRequest = scapy.ARP(pdst=ip)
    print(arpRequest.summary())
    
scan("192.168.42.2/24")