#!/usr/bin/env python3

import subprocess
import optparse
import re

def getArgs():
    parser = optparse.OptionParser()

    parser.add_option("-i", "--interface", dest="interface", help="Interface to change")
    parser.add_option("-m", "--mac", dest="newMac", help="New MAC Address")
    
    options, arguments = parser.parse_args()
    
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info.")
    elif not options.newMac:
        parser.error("[-] Please specify a MAC address, use --help for more info.")

    return options

def changeMac(interface, newMac):
    print(f"[+] Changing MAC address for {interface} to {newMac}")

    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", newMac])
    subprocess.call(["ifconfig", interface, "up"])

if __name__ == "__main__":
    options = getArgs()
    changeMac(options.interface, options.newMac)
    
    ifconfigResult = subprocess.check_output(["ifconfig", options.interface])
    macSearchResult = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfigResult))
    
    if not macSearchResult:
        print("[-] Could not read MAC Address")
        exit(1)
    
    print(macSearchResult.group(0))