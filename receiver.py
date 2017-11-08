#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 13:08:50 2017

@author: ryanthebling
"""

import socket
import time

packet_size = 2048
tcp_data_list = []
udp_data_list = []

s_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

receiver_ip = '127.0.0.1'
receiver_port_tcp = 7777
receiver_port_udp = 7778

s_tcp.bind((receiver_ip, receiver_port_tcp))
s_udp.bind((receiver_ip, receiver_port_udp))

def extract_data(input_list, seq_num, data):
    if (seq_num == len(input_list)):
        input_list.append(data)
    elif (seq_num < len(input_list)):
        input_list[seq_num] = data
    else:
        while seq_num > len(input_list):
            input_list.append(0)
        input_list.append(data)
    return input_list
    
def find_packet_loss(packet_list):
    counter = 0
    for i in range (len(packet_list)):
        if packet_list[i] == 0:
            counter += 1
    return counter / len(packet_list)

def find_throughput(packet_list):
    while 0 in packet_list:
        packet_list.remove(0)
    maximum = 1/min(packet_list)
    minimum = 1/max(packet_list)
    average = 1 / (sum(packet_list) / len(packet_list))
    return (maximum, minimum, average)
        


s_tcp.listen(1)
conn, addr = s_tcp.accept()
with conn:
    print('connected by ', addr)
    while True:
        data = conn.recv(packet_size)
        if not data:
            break
        tcp_sequence_num = int(data[0:8])
        tcp_data_point = time.time() - float(data[8:])
        tcp_data_list = extract_data(tcp_data_list, tcp_sequence_num, tcp_data_point)
        
        #  print("tcp:",float(data), "my time:",time.time(), "diff:",time.time()-float(data))

        data = s_udp.recv(packet_size)
        if not data:
            break
        udp_sequence_num = int(data[0:8])
        udp_data_point = time.time() - float(data[8:])
        udp_data_list = extract_data(udp_data_list, udp_sequence_num, udp_data_point)
        #  print("udp:",float(data), "my time:",time.time(), "diff:",time.time()-float(data))
        
print("TCP packet loss: ", find_packet_loss(tcp_data_list)*100, "%")
print("UDP packet loss: ", find_packet_loss(udp_data_list)*100, "%")
print("TCP throughput: ")
delay = find_throughput(tcp_data_list)
print("max: ",delay[0], "min: ",delay[1],"avg: ",delay[2])
print("UDP throughput: ")
delay = find_throughput(udp_data_list)
print("max: ",delay[0], "min: ",delay[1],"avg: ",delay[2])


#s_udp.listen(1)

