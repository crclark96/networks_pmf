#!/usr/bin/env python3

import socket
import time
import random

num_packets = 20
packet_size = 2048
seq_num_max_len = 8
packet_loss_percentage = 15
receiver_ip = '127.0.0.1'
receiver_port_tcp = 7777
receiver_port_udp = 7778

def tcp_send():
    s_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_tcp.connect((receiver_ip, receiver_port_tcp))
    for i in range(num_packets):
        cur_time = str(time.time())
        seq_num = str(i)
        while(len(seq_num) < seq_num_max_len): # make sequence number const size
            seq_num = '0'+seq_num
        packet = seq_num+'0'*(packet_size-len(cur_time)-seq_num_max_len)+cur_time
        packet = packet.encode('ascii')
        if not (random.randint(0,100) < packet_loss_percentage):
            time.sleep(random.randint(0,100)/1000) # simulate delay
            s_tcp.sendall(packet)
    s_tcp.close()
            
def udp_send():
    s_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s_udp.connect((receiver_ip, receiver_port_udp))
    for i in range(num_packets):
        cur_time = str(time.time())
        seq_num = str(i)
        while(len(seq_num) < seq_num_max_len): # make sequence number const size
            seq_num = '0'+seq_num
        packet = seq_num+'0'*(packet_size-len(cur_time)-seq_num_max_len)+cur_time
        packet = packet.encode('ascii')
        if not (random.randint(0,100) < packet_loss_percentage):
            time.sleep(random.randint(0,100)/1000) # simulate delay
            s_udp.sendall(packet)
        print("send udp packet")
    s_udp.close()


tcp_send()
udp_send()
print("we're in")
