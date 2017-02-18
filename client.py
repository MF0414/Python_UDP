import socket
import sys

packet_size = 1024

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Connect the socket to the port where the server is listening
#Bind Socket to Port
port = sys.argv[1]
ip = sys.argv[2]
file_name = sys.argv[3]
out_file = sys.argv[4]

FILE = open(out_file, "wb")
server_address = (ip,int(port))
    # Send request
request = "r" + file_name
print("Sending Request")
sent = sock.sendto(request.encode(), server_address)

data,server = sock.recvfrom(packet_size)
run = 1
while run == 1:
   FILE.write(data)
   data, server = sock.recvfrom(packet_size)
   try:
      if(data.decode() == "halt"):
         run = 0
   except UnicodeDecodeError:
      continue

print("File Done. Closing Socket and File.")
sock.close()
FILE.close()
