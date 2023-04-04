#!/usr/bin/env python3

import socket
import sys

HOST=sys.argv[1]
PORT=int(sys.argv[2])

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    msg = s.recv(1024)
    msg = msg.decode('utf-8')
    name = msg.split()[-1]
    print('Server name is: %s' % name)
    
    s.close()
