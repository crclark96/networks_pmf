import socket
import time

num_packets = 20

s_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

receiver_ip = '128.4.124.32'
receiver_port_tcp = 7777
receiver_port_udp = 7778

s_tcp.connect((receiver_ip, receiver_port_tcp))
s_udp.connect((receiver_ip, receiver_port_udp))
for i in range(num_packets):
    s_tcp.sendall(str(time.time()).encode('ascii'))
    s_udp.sendall(str(time.time()).encode('ascii'))

s_tcp.close()
s_udp.close()

print("we're in")