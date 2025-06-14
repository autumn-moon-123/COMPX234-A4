import socket
import os
import threading

class UDPServer:
    def __init__(self, port):
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('', port))
        print(f" Server started on port {port}")
        self.active_threads = {}

    def start(self):
        while True:
            try:
                data, addr = self.sock.recvfrom(1024)
                message = data.decode().strip()
                if message.startswith("DOWNLOAD"):
  
                    parts = message.split(' ', 1)
                    if len(parts) < 2:
                        print(f"Invalid DOWNLOAD format: {message}")
                        continue

                    filename = parts[1].strip()
                    print(f" Received DOWNLOAD request for '{filename}' from {addr[0]}:{addr[1]}")


                    client_port = random.randint(50000, 51000)
                    thread = threading.Thread(
                        target=self.handle_client,
                        args=(filename, addr, client_port)
                    )
                    thread.start()
                    self.active_threads[client_port] = thread
            except Exception as e:
                print(f" Server error: {e}")
