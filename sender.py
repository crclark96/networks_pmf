#!/usr/bin/env python3

import socket
import time
import random

num_packets = 20
packet_size = 2048
seq_num_max_len = 8
packet_loss_percentage = 0
receiver_ip = '127.0.0.1'
receiver_port_tcp = 7777
receiver_port_udp = 7778
sender_ip = '127.0.0.1'
controller_port = 7780


def tcp_send():
    '''
    sender function for tcp test
    '''
    # set up socket
    s_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_tcp.connect((receiver_ip, receiver_port_tcp))

    # send packets
    for i in range(num_packets):
        cur_time = str(time.time())
        seq_num = '0'*(seq_num_max_len - len(str(i))) + str(i)
        # construct packet from seq_num, total number of packets, time sent
        # (0 padded)
        packet = seq_num
        packet += '0'*(seq_num_max_len-len(str(num_packets))) + str(num_packets)
        packet += '0'*(packet_size - len(packet) - len(cur_time))
        packet += cur_time
        packet = packet.encode('ascii')

        # randomly drop packets based on percentage defined above
        if not (random.randint(0,100) < packet_loss_percentage):
            time.sleep(random.randint(0,100)/1000) # simulate delay
            s_tcp.sendall(packet)

    # close connection once all packets are sent
    s_tcp.close()
            
def udp_send():
    # set up socket 
    s_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s_udp.connect((receiver_ip, receiver_port_udp))

    # send packets
    for i in range(num_packets):
        cur_time = str(time.time())
        seq_num = '0'*(seq_num_max_len - len(str(i))) + str(i)
        # construct packet from seq_num, total number of packets, time sent
        # (0 padded)
        packet = seq_num
        packet += '0'*(seq_num_max_len - len(str(num_packets))) + str(num_packets)
        packet += '0'*(packet_size - len(packet) - len(cur_time))+cur_time
        packet = packet.encode('ascii')

        # randomly drop packets based on percentage defined above
        if not (random.randint(0,100) < packet_loss_percentage):
            time.sleep(random.randint(0,100)/1000) # simulate delay
            s_udp.sendall(packet)

    # close connection once all packets are sent
    s_udp.close()


if __name__ == "__main__":
    # set up socket to listen to controller
    controller = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    controller.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    controller.bind((sender_ip, controller_port))
    controller.listen(1)

    # accept incoming connection
    conn,addr = controller.accept()
    with conn:
        while True:
            data = conn.recv(packet_size)
            if not data:
                break
            if int(data) == 1:
                print("tcp send")
                tcp_send()
            elif int(data) == 2:
                print("udp send")
                udp_send()
