import socket

# create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind the socket to port 85
server_address = ('localhost', 85)
sock.bind(server_address)

# listen for incoming connections
sock.listen(1)

# main loop to handle incoming connections
while True:
    # wait for a connection
    connection, client_address = sock.accept()

    try:
        # receive data from the connection
        data = connection.recv(1024)

        # check if the received packet has a SYN flag set
        if data and data[13] & 0x02:
            # construct the RST packet
            ip_header = data[:12]
            tcp_header = struct.pack('!HHIIBBHHH', 85, client_address[1], 0, 0, 5, 0, 8192, 0, 0)
            rst_packet = ip_header + tcp_header

            # send the RST packet to the client
            sock.sendto(rst_packet, client_address)

            # log the event for security purposes
            print(f"Received SYN flag on port 85 from {client_address[0]}. Responded with RST packet.")

    finally:
        # close the connection
        connection.close()
