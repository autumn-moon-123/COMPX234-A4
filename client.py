
import socket
import sys
import os
import base64
import random

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind(('127.0.0.1', 12346))  

filename = input("filename: ")
client.sendto(filename.encode(), ('127.0.0.1', 12345))

with open('downloaded_' + filename, 'wb') as f:
    f.write(client.recvfrom(65535)[0])
