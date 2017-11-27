#!/usr/bin/env python3
import socket
import sys
import time

packet_size = 2048
sender_ip = '127.0.0.1'
sender_port = 7780
receiver_ip = '127.0.0.1'
receiver_port = 7779

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

if __name__ == "__main__":
    # initialize sockets for sender and receiver
    s_rcv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_snd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_rcv.connect((receiver_ip, receiver_port))
    s_snd.connect((sender_ip, sender_port))

    # explain cli usage
    if len(sys.argv) != 2:
        print("usage: controller.py --[tcp,udp]")
        sys.exit()
    
    if sys.argv[1] == '--tcp':
        packet = '0'*(packet_size-1)+'1'
    elif sys.argv[1] == '--udp':
        packet = '0'*(packet_size-1)+'2'
    else:
        print("usage: controller.py --[tcp,udp]")
        sys.exit()

    # create packet and send to receiver and listener
    packet = packet.encode('ascii')
    s_rcv.sendall(packet)
    time.sleep(1) # wait for receiver to set up servers
    s_snd.sendall(packet)

    received_packet = s_rcv.recv(packet_size)
    print(received_packet)
    received_packet = eval(received_packet)

    if sys.argv[1] == '--tcp':
        print("TCP packet loss: ", find_packet_loss(received_packet)*100, "%")
        print("TCP throughput: ")
        # calculate total throughput
        delay = find_throughput(received_packet)
        print("max: ",delay[0], "min: ",delay[1],"avg: ",delay[2])
    else:
        print("UDP packet loss: ", find_packet_loss(received_packet)*100, "%")
        print("UDP throughput: ")
        # calculate total throughput
        delay = find_throughput(received_packet)
        print("max: ",delay[0], "min: ",delay[1],"avg: ",delay[2])

    s_snd.close()
    s_rcv.close()

