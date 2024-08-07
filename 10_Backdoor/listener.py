import socket

listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

listener.bind(("192.168.42.128", 4444))
listener.listen(0)
print("[+] Waiting for incoming connections.")

connection, address = listener.accept()
print("[+] Got a connection from {address}.")