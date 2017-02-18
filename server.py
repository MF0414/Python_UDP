import socket
import sys

#...........................................................#
packet_size = 1024
window_size = 5
header_size = 3
port = int(sys.argv[1])
#...........................................................#


def send_packet(socket, packet, client_address, header):

   #Build Header and Send Packet
   ack_response = "ACK" + header
   header = bin(header)
   packet.append(header)
   sent = socket.sendto(packet, client_address)
   
   # Checks for Acknowledgment
   try:
      data, client_address = socket.recvfrom(packet_size)
      if data.decode() == ack_response:
         return 1
   except Exception:
      return 0


if __name__ == '__main__':
   #Create Socket
   try:
      sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
   except Exception:
      print("Socket Creation Failed. Exiting...")
      sys.exit()

   #Check Validity of Port
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
   
      # Read in a Window of Packets
      window = []
      for i in range(window_size):
         try:
            packet = FILE.read(packet_size - header_size)
         except Exception:
            print("File Read Failure. Exiting...")
            sys.exit()
         window.append(packet)

      #Send Packets 
      for i in range(len(window)):
         print("Sending %s Packets.\n" % (len(window)))
         if window[i]:
            acknowledged = 0
            while acknowledged == 0: 
               acknowledged = send_packet(sock, window[i], address, i)
         else:
            acknowledged = 0
            while acknowledged == 0:
               acknowledged = send_packet(sock, "halt".encode(), address, i)
            run = 0

   print("File Transfer Finished.\n")


