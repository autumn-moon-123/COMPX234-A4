import socket
import threading
import os
import random
import base64
import sys  

class UDPServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind((host, port))
        self.file_dir = os.getcwd()

        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server.bind(('127.0.0.1', 12345))

    def handle_download_request(self, data, client_addr):
         request = data.decode().strip()
         if not request.startswith("DOWNLOAD "):
          return
    
filename = server.recvfrom(1024)[0].decode()
with open(filename, 'rb') as f:
        server.sendto(f.read(), ('127.0.0.1', 12346)) 