#!/usr/bin/env python

"""
    server-drop-data.py accepts TCP connections on TCP_IP:TCP_PORT and receives
    and discards all incoming data. It prints the estimated incoming bandwidth
    once per second for each active connection.
"""

import socket
import sys
import time
from thread import start_new_thread

TCP_IP = '127.0.0.1' 
TCP_PORT = 5005

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
print('Started listening on: ' + TCP_IP + ':' + str(TCP_PORT))

def client_thread(conn, addr):
    counted = 0
    last_sec = int(time.time())
    while True:
        data = conn.recv(1024*1024)
        if not data:
            break
        counted = counted + len(data)
        current_sec = int(time.time())
        if current_sec != last_sec:
            secs_gone = current_sec - last_sec
            estimate = counted / secs_gone
            estimate = estimate * 8
            estimate = estimate / 1024
            estimate = estimate / 1024
            print('Estimated bandwidth on ' + addr[0] + ':' + str(addr[1]) + ' is ' + str(estimate) + ' Mbit/s')
            last_sec = current_sec
            counted = 0
    print('Closed connection to ' + addr[0] + ':' + str(addr[1]))

while True:
    try:
        conn, addr = s.accept()
        print('Accepted connection from ' + addr[0] + ':' + str(addr[1]))
        start_new_thread(client_thread, (conn, addr, ))
    except KeyboardInterrupt:
        conn.close()
        sys.exit()

