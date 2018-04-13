#!/usr/bin/env python3

"""
    client-alternate-speed.py connects to TCP_IP:TCP_PORT and emits data 
    at TARGET_SEND_RATE_1 for INTERVAL_1 seconds and TARGET_SEND_RATE_2
    for INTERVAL_2 seconds alternatingly.
"""

import socket
import sys
import termios
import time
import tty
from _thread import start_new_thread

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
TARGET_SEND_RATE_1 = 30.0
TARGET_SEND_RATE_2 = 150.0
INTERVAL_1 = 10
INTERVAL_2 = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.connect((TCP_IP, TCP_PORT))

mbit_chunk = b'\60' * 1024 * 128
sleep_interval = 0.1

def send_thread(s):
    while True:
        sent = s.send(mbit_chunk)
        time.sleep(sleep_interval)

start_new_thread(send_thread, (s,))

while True:
    print('Emitting ' + str(TARGET_SEND_RATE_1) + ' MBit/s')
    sleep_interval = 1/TARGET_SEND_RATE_1
    time.sleep(INTERVAL_1)
    print('Emitting ' + str(TARGET_SEND_RATE_2) + ' MBit/s')
    sleep_interval = 1/TARGET_SEND_RATE_2
    time.sleep(INTERVAL_2)
