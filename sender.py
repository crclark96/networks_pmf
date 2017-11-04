import socket
import time

num_packets = 20
packet_size = 2048

s_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

receiver_ip = '127.0.0.1'
receiver_port_tcp = 7777
receiver_port_udp = 7778

s_tcp.connect((receiver_ip, receiver_port_tcp))
s_udp.connect((receiver_ip, receiver_port_udp))
for i in range(num_packets):
    cur_time = str(time.time())
    packet = '0'*(packet_size-len(cur_time))+cur_time
    packet = packet.encode('ascii')
    s_tcp.sendall(packet)
    s_udp.sendall(packet)

s_tcp.close()
s_udp.close()

print("we're in")
