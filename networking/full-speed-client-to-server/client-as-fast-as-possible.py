#!/usr/bin/env python3

"""
    client-as-fast-as-possible.py connects to TCP_IP:TCP_PORT and emits data
    as fast as possible.
"""

import socket
import sys

TCP_IP = '127.0.0.1'
TCP_PORT = 5005

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.connect((TCP_IP, TCP_PORT))

chunk = b'\60' * 1024 * 1024

while True:
    try:
        sent = s.send(chunk)
    except KeyboardInterrupt:
        s.close()
        sys.exit()
