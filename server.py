import socket
import sys

#...........................................................#
packet_size = 1024
window_size = 5
#...........................................................#


#Create Socket
try:
   sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except Exception:
   print("Socket Creation Failed. Exiting...")
   sys.exit()

#Check Validity of Port
port = int(sys.argv[1])
if port < 0 or port > 65535:
   print("Port Number is Invalid. Exiting...")
   sys.exit()

#Bind Socket
try:
   server_address = ('localhost',port)
   sock.bind(server_address)
except Exception:
   print("Socket Binding Failed. Exiting...")
   sys.exit()

#Receive Requests
print("Ready to Receive Requests.")

try:
data, address = sock.recvfrom(packet_size)
if data[:1] == "r".encode():
   file_name = str(data.decode()[1:])
   FILE = open(file_name,"rb")
except Exception:
   print("Receive Failed. Exiting...")
   sys.exit()

#Process Requests
run = 1
while run == 1:
   window = []
   for i in range(window_size):
      packet = FILE.read(packet_size)
      window.append(packet)

   for i in range(len(window)):
      print("Sending %s Packets.\n" % (len(window)))
      if window[i]:
         sent = sock.sendto(window[i], address)
      else:
         sent = sock.sendto("halt".encode(), address)
         run = 0

print("File Transfer Finished.\n")


