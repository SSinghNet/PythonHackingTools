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

def getCurrentMac(interface):
    ifconfigResult = subprocess.check_output(["ifconfig", interface])
    macSearchResult = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfigResult))
    
    if not macSearchResult:
        exit("[-] Could not read interface's current MAC Address.")
    
    return macSearchResult.group(0)

if __name__ == "__main__":
    args = getArgs()
    
    currentMac = getCurrentMac(args.interface)
    print(f"Current MAC: {currentMac}")
    
    changeMac(args.interface, args.newMac)
    
    currentMac = getCurrentMac(args.interface)
    if currentMac == args.newMac:
        print (f"[+] MAC address of {args.interface} was successfully changed to {currentMac}")
    else:
        print (f"[-] MAC address of {args.interface} was not changed.")
    