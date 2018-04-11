#!/usr/bin/env python3

"""
    client-defined-speed.py connects to TCP_IP:TCP_PORT and emits data at a  
    rate somewhere near TARGET_SEND_RATE_MBPS. TODO 
"""

import socket
import sys
import termios
import time
import tty
from _thread import start_new_thread

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
TARGET_SEND_RATE = [0.0, 5.0, 50.0, 150.0]

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def print_usage():
    print('Press \'q\' to quit, \'1\' for no transmission and \'2\'-\'4\' for different data rates (' + str(TARGET_SEND_RATE[1:]) + ' MBit/s)')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.connect((TCP_IP, TCP_PORT))

mbit_chunk = b'\60' * 1024 * 128
active = False
sleep_interval = 0.1

def send_thread(s):
    while True:
        if active:
            sent = s.send(mbit_chunk)
            time.sleep(sleep_interval)

start_new_thread(send_thread, (s,))
print_usage()
while True:
    x = getch()
    if x == '1':
        print('Transmission off')
        active = False
        sleep_interval = 0.1
    elif x == '2' or x == '3' or x == '4':
        index = int(x)-1
        active = True
        print('Emitting ' + str(TARGET_SEND_RATE[index]) + ' MBit/s')
        sleep_interval = 1/(TARGET_SEND_RATE[index])
    elif x == 'q':
        s.close()
        sys.exit()
    else:
        print_usage()
