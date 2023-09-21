import socket


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


server_address = ('localhost', 85)
sock.bind(server_address)


sock.listen(1)


while True:
  
    connection, client_address = sock.accept()

    try:
       
        data = connection.recv(1024)

       
        if data and data[13] & 0x02:
           
            ip_header = data[:12]
            tcp_header = struct.pack('!HHIIBBHHH', 85, client_address[1], 0, 0, 5, 0, 8192, 0, 0)
            rst_packet = ip_header + tcp_header

            
            sock.sendto(rst_packet, client_address)

           
            print(f"Received SYN flag on port 85 from {client_address[0]}. Responded with RST packet.")

    finally:
   
        connection.close()
