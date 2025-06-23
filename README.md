UDP File transfer system
This is a simple file transfer system based on the UDP protocol, consisting of client-side and server-side components. The system supports multi-threaded processing and is capable of efficiently transferring files.

System Architecture
Server side: Listen to the specified port and handle file download requests
Client: Connect to the server and request to download the files in the file list

Functional features:
Support batch downloading of multiple files
File block transmission
Data transmission uses Base64 encoding
Random port allocation avoids conflicts
Display the download progress in real time
A perfect error handling mechanism

Installation and Usage
Environmental requirements
Python 3.6+
No additional dependencies are needed.

File structure
text
udp-file-transfer/
├── Server.py # server program
├── Client.py # client program
└── filelist.txt # List of Sample Files (for client use)

The downloaded file will be saved in the format of downloaded_< original file name >

Usage example:
Server side
bash:
# Start the server in Terminal 1
$ python server.py 54321
Server started on port 54321

Client side
bash:
# Start the client in Terminal 2
$ python client.py localhost 54321 filelist.txt
Received 512/2048 bytes
Received 1024/2048 bytes
Received 1536/2048 bytes
Received 2048/2048 bytes
Download completed: 1/1 files

Agreement Description
Client → Server (Initial Request)
DOWNLOAD <filename>
Server response
The file exists:
OK <filename> SIZE <filesize> PORT <dataport>
The file does not exist:
ERR <filename> NOT_FOUND
Data Transmission Protocol
The client requests data blocks:
FILE <filename> GET START <start> END <end>
Server response data:
FILE <filename> OK START <start> END <end> DATA <base64_data>
Close the connection
FILE <filename> CLOSE
Response:
FILE <filename> CLOSE_OK

Notes:
The server and the client need to be in the same network environment
The firewall needs to allow communication on the specified UDP port
The file names in the file list need to exactly match the file names on the server
The downloaded files will be saved in the current working directory of the client
Large file transfer may take a relatively long time (a feature of the UDP protocol)
