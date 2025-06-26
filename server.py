import socket
import threading
import os
import random
import base64
import sys  

class UDPServer:
    """A UDP server that handles file download requests from clients."""
    def __init__(self, host, port):
        """
        Initialize the UDP server.
        
        Args:
            host (str): Host interface to bind to
            port (int): Port number to listen on
        """
        self.host = host
        self.port = port
        # Create and bind main server socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind((host, port))
        # Serve files from current directory
        self.file_dir = os.getcwd()

    def handle_download_request(self, data, client_addr):
         """
        Handle an incoming download request from a client.
        
        Args:
            data (bytes): The received data from client
            client_addr (tuple): Client address (host, port)
         """
         request = data.decode().strip()
         if not request.startswith("DOWNLOAD "):
          return # Ignore malformed requests
         filename = request[9:]
         filepath = os.path.join(self.file_dir, filename)
        # Check if file exists
         if not os.path.exists(filepath):
            self.server_socket.sendto(f"ERR {filename} NOT_FOUND".encode(), client_addr)
            return
        # Create random port for data transfer (50000-51000)
         data_port = random.randint(50000, 51000)
         data_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
         data_socket.bind((self.host, data_port))

        # Send file info back to client
         file_size = os.path.getsize(filepath)
         self.server_socket.sendto(f"OK {filename} SIZE {file_size} PORT {data_port}".encode(), client_addr)
        # Start new thread to handle file transfer
         threading.Thread(
            target=self.handle_file_transfer,
            args=(filename, filepath, data_socket),
            daemon=True
        ).start()
    def handle_file_transfer(self, filename, filepath, data_socket):
        """
        Handle the actual file transfer to the client in chunks.
        
        Args:
            filename (str): Name of the file being transferred
            filepath (str): Path to the file on server
            data_socket (socket): Socket for data transfer
        """
        try:
            while True:
                # Wait for client request
                data, client_addr = data_socket.recvfrom(1024)
                request = data.decode()
                # Handle data chunk request
                if request.startswith(f"FILE {filename} GET"):
                    parts = request.split()
                    start = int(parts[4])
                    end = int(parts[6])

                    with open(filepath, 'rb') as f:
                        f.seek(start)
                        # Read requested byte range
                        data_block = f.read(end - start + 1)
                        # Encode as base64 for transmission
                        encoded = base64.b64encode(data_block).decode()
                        response = f"FILE {filename} OK START {start} END {end} DATA {encoded}"
                        data_socket.sendto(response.encode(), client_addr)
                # Handle close request
                elif request == f"FILE {filename} CLOSE":
                    data_socket.sendto(f"FILE {filename} CLOSE_OK".encode(), client_addr)
                    break
        finally:
         data_socket.close()
    def start(self):
        """Start the server and begin listening for requests."""
        while True:
            data, client_addr = self.server_socket.recvfrom(1024)
            threading.Thread(
                target=self.handle_download_request,
                args=(data, client_addr),
                daemon=True
            ).start()
if __name__ == "__main__":
    # Validate command line arguments
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