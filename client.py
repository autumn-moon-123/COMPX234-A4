
import socket
import sys
import os
import base64
import random


class UDPClient:
    def __init__(self, server_host, server_port, filelist):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_host = server_host
        self.server_port = server_port
        self.filelist = filelist
        self.download_dir = os.getcwd()
    def download_file(self, filename):
        self.client_socket.sendto(f"DOWNLOAD {filename}".encode(), (self.server_host, self.server_port))
        response, _ = self.client_socket.recvfrom(1024)
        response = response.decode()

        if response.startswith("ERR"):
            print(f"ERR {filename} NOT_FOUND")
            return False
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client.bind(('127.0.0.1', 12346))  

        filename = input("filename: ")
        client.sendto(filename.encode(), ('127.0.0.1', 12345))

        with open('downloaded_' + filename, 'wb') as f:
            f.write(client.recvfrom(65535)[0])
