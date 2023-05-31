#!/usr/bin/env python3

	#CLIENT
import socket
import sys

HOST = '127.0.0.1'
PORT = 8080	#Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

	#connection: operazione per contattare un server in listen
	s.connect((HOST, PORT))

	msg = input('Please enter the message: ')  
	s.sendall(msg.encode('utf-8'))
	#data = s.recv(1024)
	s.close()

	#print('Received: %s'% data.decode('utf-8'))
