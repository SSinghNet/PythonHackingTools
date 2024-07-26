#!usr/bin/env python3

# iptables -I FORWARD -j NFQUEUE --queue-num [queueNum]

import netfilterqueue

def process_packet(packet):
    print(packet)

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()