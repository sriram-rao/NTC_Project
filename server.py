import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 10000))
server.listen(5)

while True:
  connection, address = server.accept()
  buff = connection.recv(1024)
  if len(buff) > 0:
    print buff
    server.send(str(2**64 - 1))
    break;


