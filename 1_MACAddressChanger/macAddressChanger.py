#!/usr/bin/env python

import subprocess

interface = "wlan0"
newMac = "00:11:22:33:44:77"

subprocess.call("ifconfig " + interface + " down", shell=True)
subprocess.call("ifconfig " + interface + " hw ether " + newMac, shell=True)
subprocess.call("ifconfig " + interface + " up", shell=True)