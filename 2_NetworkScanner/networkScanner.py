#!usr/bin/env python
import scapy.all as scapy

def scan(ip):
    scapy.arping(ip)
    
scan("192.168.42.2")