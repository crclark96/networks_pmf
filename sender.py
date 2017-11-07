import socket
import time
import random

num_packets = 20
packet_size = 2048
seq_num_max_len = 8
packet_loss_percentage = 15

s_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

receiver_ip = '127.0.0.1'
receiver_port_tcp = 7777
receiver_port_udp = 7778

s_tcp.connect((receiver_ip, receiver_port_tcp))
s_udp.connect((receiver_ip, receiver_port_udp))
for i in range(num_packets):
    cur_time = str(time.time())
    seq_num = str(i)
    while(len(seq_num) < seq_num_max_len): #make sequence number constant size
        seq_num = '0'+seq_num
    packet = seq_num+'0'*(packet_size-len(cur_time)-seq_num_max_len)+cur_time
    packet = packet.encode('ascii')
    if not (random.randint(0,100) < packet_loss_percentage):
        s_tcp.sendall(packet)
        s_udp.sendall(packet)

s_tcp.close()
s_udp.close()

print("we're in")
