#!/usr/bin/env python3

"""
    server-no-read.py accepts TCP connections on TCP_IP:TCP_PORT but doesn't 
    read from those connections. 
"""

import socket

TCP_IP = '127.0.0.1' 
TCP_PORT = 5005

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
print('Started listening on: ' + TCP_IP + ':' + str(TCP_PORT))

while True:
    conn, addr = s.accept()
    print('Accepted connection from ' + addr[0] + ':' + str(addr[1]))

conn.close()