#!/usr/bin/env python3

"""
    client-fill-up-send-buffer.py connects to TCP_IP:TCP_PORT via TCP and 
    pushes data chunks (with length chunk_size, consisting of only ASCII '0')
    to the send buffer.

    If the server doesn't acknowledge any data (server-noread-py does that), 
    client-fill-up-send-buffer.py should push bytes until the send buffer is full 
    and then block within s.send().
"""

import random
import socket
import string
import time

TCP_IP = '127.0.0.1'
TCP_PORT = 5005

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.connect((TCP_IP, TCP_PORT))

send_buf_size = s.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
chunk_size = send_buf_size / 16
if chunk_size > 128*1024:
    chunk_size = 128*1024
print("Socket send buffer size = " + str(send_buf_size))
print("Chunk size = " + str(chunk_size))

total = 0
while True:
    sent = s.send(b'\60' * chunk_size)
    total = total + sent
    print("Totally pushed bytes = " + str(total))

s.close()

