#!/usr/bin/env python3

import subprocess
import optparse

def getArgs():
    parser = optparse.OptionParser()

    parser.add_option("-i", "--interface", dest="interface", help="Interface to change")
    parser.add_option("-m", "--mac", dest="newMac", help="New MAC Address")
    
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info.")
    elif not options.newMac:
        parser.error("[-] Please specify a MAC address, use --help for more info.")

    return parser.parse_args()

def changeMac(interface, newMac):
    print(f"[+] Changing MAC address for {interface} to {newMac}")

    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", newMac])
    subprocess.call(["ifconfig", interface, "up"])

if __name__ == "__main__":
    options, arguments = getArgs()
    changeMac(options.interface, options.newMac)