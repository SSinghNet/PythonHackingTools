#!usr/bin/env python
import optparse
import scapy.all as scapy

def getArgs():
    parser = optparse.OptionParser()

    parser.add_option("-r", "--iprange", dest="ipRange", help="IP Range to Scan")
    
    options, arguments = parser.parse_args()
    
    if not options.ipRange:
        parser.error("[-] Please specify an IP range, use --help for more info.")

    return options

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
    rowFormat = "{: ^16} | {: ^18}"
    
    print()
    
    print(rowFormat.format("IP", "MAC Address"))
    print("{:-^16}-|-{:-^18}".format("",""))
    for client in clients:
        print(rowFormat.format(client["ip"], client["mac"]))
    
    print()
    
options = getArgs()
clients = scan(options.ipRange)
printResult(clients)