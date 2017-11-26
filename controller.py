#!/usr/bin/env python3
import socket
import sys
import time

packet_size = 2048
sender_ip = '127.0.0.1'
sender_port = 7780
receiver_ip = '127.0.0.1'
receiver_port = 7779

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

    s_snd.close()
    s_rcv.close()
