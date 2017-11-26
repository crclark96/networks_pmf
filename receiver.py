#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 13:08:50 2017

@author: ryanthebling
"""

import socket
import time

packet_size = 2048

receiver_ip = '127.0.0.1'
receiver_port_tcp = 7777
receiver_port_udp = 7778
controller_port = 7779

# set up listening ports 
s_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s_tcp.bind((receiver_ip, receiver_port_tcp))
s_tcp.listen(1)

s_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s_udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s_udp.bind((receiver_ip, receiver_port_udp))

def extract_data(input_list, seq_num, data):
    '''
    place transmission times in correct place in list, expand list if necessary
    '''
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
    '''
    count number of empty (missing) packets in packet list
    '''
    counter = 0
    for i in range (len(packet_list)):
        if packet_list[i] == 0:
            counter += 1
    return counter / len(packet_list)

def find_throughput(packet_list):
    '''
    calculate throughput based on transmission times list
    '''
    while 0 in packet_list:
        packet_list.remove(0) # remove missing packets from list
    maximum = 1/min(packet_list)
    minimum = 1/max(packet_list)
    average = 1 / (sum(packet_list) / len(packet_list))
    return (maximum, minimum, average)
        
def tcp_receive():
    '''
    tcp receiver method
    '''
    tcp_data_list = [] # initialize list to place transmission times
    conn, addr = s_tcp.accept() # accept connections
    with conn:
        print('connected by ', addr)
        while True:
            data = conn.recv(packet_size)
            if not data:
                break
            # break packet into data chunks
            tcp_sequence_num = int(data[0:8])
            tcp_num_packets = int(data[8:16])
            
            # calculate transmission time
            tcp_data_point = time.time() - float(data[16:])

            # add to list
            tcp_data_list = extract_data(tcp_data_list, \
                                         tcp_sequence_num, \
                                         tcp_data_point)
            # terminate at last packet
            if tcp_sequence_num == tcp_num_packets-1:
                break
            
    print("TCP packet loss: ", find_packet_loss(tcp_data_list)*100, "%")
    print("TCP throughput: ")
    # calculate total throughput
    delay = find_throughput(tcp_data_list)
    print("max: ",delay[0], "min: ",delay[1],"avg: ",delay[2])



def udp_receive():
    '''
    udp receiver method
    '''
    udp_data_list = [] # initialize list to place transmission times
    while True:
        data = s_udp.recv(packet_size)
        if not data:
            break
        # break packet into data chunks
        udp_sequence_num = int(data[0:8])
        udp_num_packets = int(data[8:16])

        #calculate transmission time
        udp_data_point = time.time() - float(data[16:])

        # add to list
        udp_data_list = extract_data(udp_data_list, \
                                     udp_sequence_num, \
                                     udp_data_point)
        # terminate at last packet
        if udp_sequence_num == udp_num_packets-1:
            break
    print("UDP packet loss: ", find_packet_loss(udp_data_list)*100, "%")
    print("UDP throughput: ")
    # calculate total throughput
    delay = find_throughput(udp_data_list)
    print("max: ",delay[0], "min: ",delay[1],"avg: ",delay[2])


if __name__ == "__main__":
    # initialize controller socket
    controller = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    controller.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    controller.bind((receiver_ip, controller_port))
    controller.listen(1)

    conn,addr = controller.accept()
    with conn:
        while True:
            data = conn.recv(packet_size)
            if not data:
                break
            if int(data) == 1:
                print("tcp receive")
                tcp_receive()
            elif int(data) == 2:
                print("udp receive")
                udp_receive()
