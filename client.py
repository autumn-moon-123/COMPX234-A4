import socket
import sys
import os
import base64
import random


class UDPClient:
    """A UDP client for downloading files from a server in chunks."""
    def __init__(self, server_host, server_port, filelist):
        """
        Initialize the UDP client.
        
        Args:
            server_host (str): The server hostname or IP address
            server_port (int): The server port number
            filelist (list): List of files to download
        """
        # Create UDP socket        
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_host = server_host
        self.server_port = server_port
        self.filelist = filelist
        # Store downloaded files in current working directory
        self.download_dir = os.getcwd()
    def download_file(self, filename):
        """
        Download a single file from the server.
        
        Args:
            filename (str): Name of the file to download
            
        Returns:
            bool: True if download succeeded, False otherwise
        """
        # Send download request to server
        self.client_socket.sendto(f"DOWNLOAD {filename}".encode(), (self.server_host, self.server_port))
        # Wait for server response
        response, _ = self.client_socket.recvfrom(1024)
        response = response.decode()
        # Check if file not found error
        if response.startswith("ERR"):
            print(f"ERR {filename} NOT_FOUND")
            return False
        # Parse server response: OK filename SIZE filesize PORT dataport
        parts = response.split()
        filename = parts[1]
        file_size = int(parts[3])
        data_port = int(parts[5])
        # Create new socket for data transfer with larger buffer
        data_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        data_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65536)
        client_port = random.randint(51000, 52000)
        data_socket.bind(('0.0.0.0', client_port))
        # Create output file path
        file_path = os.path.join(self.download_dir, f"downloaded_{filename}")
        bytes_received = 0
        block_size = 512  
        # Download file in chunks
        with open(file_path, 'wb') as f:
            while bytes_received < file_size:
                # Calculate byte range for next chunk
                start = bytes_received
                end = min(bytes_received + block_size - 1, file_size - 1)
                data_socket.sendto(f"FILE {filename} GET START {start} END {end}".encode(),
                                   (self.server_host, data_port))

                response, _ = data_socket.recvfrom(65536)
                response = response.decode()

                if response.startswith(f"FILE {filename} OK"):
                    data = base64.b64decode(response.split("DATA ")[1].encode())
                    f.write(data)
                    bytes_received += len(data)
                    print(f"Received {bytes_received}/{file_size} bytes")

            data_socket.sendto(f"FILE {filename} CLOSE".encode(), (self.server_host, data_port))
            data_socket.recvfrom(1024)  

        return bytes_received == file_size

    def download_files(self):
        """Download all files in the filelist and report completion status."""
        success = 0
        for filename in self.filelist:
            if self.download_file(filename.strip()):
                success += 1
        print(f"Download completed: {success}/{len(self.filelist)} files")
if __name__ == "__main__":
    # Command line argument validation
    if len(sys.argv) != 4: 
        print("Usage: python client.py <host> <port> <filelist>")
        sys.exit(1)

    try:
        # Read file list from input file
        with open(sys.argv[3]) as f:
            filelist = [line.strip() for line in f if line.strip()]
        # Create and run client
        client = UDPClient(sys.argv[1], int(sys.argv[2]), filelist)
        client.download_files()
    except FileNotFoundError:
        print(f"Error: File {sys.argv[3]} not found")
        sys.exit(1)
    except ValueError:
        print("Error: Port must be a valid integer")
        sys.exit(1)