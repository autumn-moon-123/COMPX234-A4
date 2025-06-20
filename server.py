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
         filename = request[9:]
         filepath = os.path.join(self.file_dir, filename)

         if not os.path.exists(filepath):
            self.server_socket.sendto(f"ERR {filename} NOT_FOUND".encode(), client_addr)
            return

         data_port = random.randint(50000, 51000)
         data_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
         data_socket.bind((self.host, data_port))

         file_size = os.path.getsize(filepath)
         self.server_socket.sendto(f"OK {filename} SIZE {file_size} PORT {data_port}".encode(), client_addr)

         threading.Thread(
            target=self.handle_file_transfer,
            args=(filename, filepath, data_socket),
            daemon=True
        ).start()
    def handle_file_transfer(self, filename, filepath, data_socket):
        try:
            while True:
                data, client_addr = data_socket.recvfrom(1024)
                request = data.decode()
                if request.startswith(f"FILE {filename} GET"):
                    parts = request.split()
                    start = int(parts[4])
                    end = int(parts[6])

                    with open(filepath, 'rb') as f:
                        f.seek(start)
                        data_block = f.read(end - start + 1)
                        encoded = base64.b64encode(data_block).decode()
                        response = f"FILE {filename} OK START {start} END {end} DATA {encoded}"
                        data_socket.sendto(response.encode(), client_addr)
                elif request == f"FILE {filename} CLOSE":
                    data_socket.sendto(f"FILE {filename} CLOSE_OK".encode(), client_addr)
                    break
        finally:
         data_socket.close()
    def start(self):
        while True:
            data, client_addr = self.server_socket.recvfrom(1024)
            threading.Thread(
                target=self.handle_download_request,
                args=(data, client_addr),
                daemon=True
            ).start()
if __name__ == "__main__":
    if len(sys.argv) != 2:  
        print("Usage: python server.py <port>")
        sys.exit(1)

    try:
        port = int(sys.argv[1])
        server = UDPServer('0.0.0.0', port)
        print(f"Server started on port {port}")
        server.start()
    except ValueError:
        print("Error: Port must be a valid integer")
        sys.exit(1)