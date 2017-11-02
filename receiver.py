# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 13:08:50 2017

@author: ryanthebling
"""

import socket

s_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

receiver_ip = '127.0.0.1'
receiver_port_tcp = 7777
receiver_port_udp = 7778

s_tcp.bind((receiver_ip, receiver_port_tcp))
s_udp.bind((receiver_ip, receiver_port_udp))

s_tcp.listen(1)
conn, addr = s_tcp.accept()
with conn:
    print('connected by ', addr)
    while True:
        data = conn.recv(1024)        
        if not data:
            break
        print(data)
        



#s_udp.listen(1)

