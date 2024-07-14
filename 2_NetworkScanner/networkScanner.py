#!usr/bin/env python
import scapy.all as scapy

def scan(ip):
    arpRequest = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arpRequestBroadcast = broadcast/arpRequest
    
    answered = scapy.srp(arpRequestBroadcast, timeout=1, verbose=False)[0]
    
    clients = []
    for i in answered:
        clients.append({"ip": i[1].psrc, "mac": i[1].hwsrc})
    return clients

def printResult(clients):
    print("IP\t\t\tMAC Address\n--------------------------------------------")
    for client in clients:
        print(f"{client['ip']}\t\t{client['mac']}")
    
clients = scan("192.168.42.2/24")
printResult(clients)