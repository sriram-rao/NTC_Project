import socket
import json

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 10000))
client.send(str(2**64-1))
print client.recv(1024)
