import socket

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(('127.0.0.1', 12345))

filename = server.recvfrom(1024)[0].decode()
with open(filename, 'rb') as f:
    server.sendto(f.read(), ('127.0.0.1', 12346)) 