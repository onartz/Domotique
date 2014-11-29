import socket
 
MCAST_GRP = '239.255.255.250'
MCAST_PORT = 1234
 
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
sock.sendto("Hello World", (MCAST_GRP, MCAST_PORT))
