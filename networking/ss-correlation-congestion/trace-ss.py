#!/usr/bin/env python

import os
import time
from datetime import datetime 

#filename = 'trace_ss_' + time.strftime('%Y-%m-%d-%H-%M-%S') + '.csv'
filename = 'current.csv'
print('Writing output to "' + filename + '"')

while True:
    cmd = '/home/stefan/development/iproute2/misc/ss -tin -o state established dst 213.209.106.95 | grep bbr | ' + \
            'sed "s/^[ \t]*//" | sed "s/[a-zA-Z:_]//g" | sed "s/[()\/ ]/,/g" | sed "s/^[ \t]*//" | sed "s/,,/,/g" | ' + \
            'sed "s/,,/,/g" | sed "s/^[,]//" >> ' + filename
    os.system(cmd)
    time.sleep(1)
