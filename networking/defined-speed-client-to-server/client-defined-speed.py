#!/usr/bin/env python3

"""
    client-defined-speed.py connects to TCP_IP:TCP_PORT and emits data at a  
    rate somewhere near TARGET_SEND_RATE_MBPS.
"""

import socket
import sys
import time

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
TARGET_SEND_RATE_MBPS = 30

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.connect((TCP_IP, TCP_PORT))

mbit_chunk = b'\60' * 1024 * 128
sleep_interval = 1/(TARGET_SEND_RATE_MBPS)

while True:
    try:
        sent = s.send(mbit_chunk)
        time.sleep(sleep_interval)
    except KeyboardInterrupt:
        s.close()
        sys.exit()
