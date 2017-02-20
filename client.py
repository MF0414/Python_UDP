import socket
import sys

#...............................................................#
packet_size = 1024
header_size = 3
port = int(sys.argv[1])
ip = sys.argv[2]
file_name = sys.argv[3]
out_file = sys.argv[4]
#...............................................................#

def receive_packet(socket, packet, client_address, header):
   return 0





if __name__ = '__main__':

   # Create Socket
   try:
      sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
   except Exception:
      print("Socket Creation Failed. Exiting...")
      sys.exit()

   #Check Validity of Port
   if port < 0 or port > 65535:
      print("Port Number is Invalid. Exiting...")
      sys.exit()

   #Bind Socket to Port
   try:
      server_address = (ip,port)
      sock.bind(server_address)   
   except Exception:
      print("Socket Binding Failed. Exiting...")
      sys.exit()

   #Open File to Write to
   try:
      FILE = open(out_file, "wb")
   except Exception:
      print("Save file creation failed. Exiting...")
      sys.exit()
   
   # Send request
   request = "r" + file_name
   print("Sending Request")
   sent = sock.sendto(request.encode(), server_address)

   #Receive File
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
