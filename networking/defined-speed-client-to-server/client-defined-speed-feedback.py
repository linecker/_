#!/usr/bin/env python3

"""
    client-defined-speed-feedback.py connects to TCP_IP:TCP_PORT and emits data
    at a rate somewhere near TARGET_SEND_RATE_MBPS. It prints the estimated
    emission rate once per second and uses this rate for a naive control loop.
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

# make junks 1% of the size i have to emit
chunk = b'\60' * int(TARGET_SEND_RATE_MBPS * 1024 * 128 * 0.01)
sleep_interval = 1/(TARGET_SEND_RATE_MBPS)

counted = 0
last_sec = int(time.time())
while True:
    try:
        sent = s.send(chunk)
        time.sleep(sleep_interval)
        counted = counted + len(chunk)
        current_sec = int(time.time())
        if current_sec != last_sec:
            secs_gone = current_sec - last_sec
            estimate = (counted / secs_gone) * 8 / 1024 / 1024
            error_factor = (TARGET_SEND_RATE_MBPS - estimate)/TARGET_SEND_RATE_MBPS
            sleep_interval = sleep_interval - (sleep_interval * error_factor);
            print(\
                'emiting ' + str(float("{0:.1f}".format(estimate))) + ' Mbit/s, ' + \
                'error ' + str(float("{0:.2f}".format(error_factor*100))) + ' %, ' + \
                'sleep ' + str(float("{0:.2f}".format(sleep_interval*1000))) + ' ms')
            last_sec = current_sec
            counted = 0
    except KeyboardInterrupt:
        s.close()
        sys.exit()
