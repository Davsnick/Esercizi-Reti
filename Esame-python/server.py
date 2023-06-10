#!/usr/bin/env python3

import socket
import sys
import time
import os
import re
from itertools import *

# Standard loopback interface address (localhost)
HOST = '127.0.0.1'
# Port to listen on (non-privileged ports are > 1023)
PORT = 8080

def look_and_say(seed, niter):
	seed = str(seed)
	niter = int(niter)
	arr = [seed]

	def get_sequence(arr, niter, seed):
		if niter == 0:
			return arr
		else:
			current = ''.join(str(len(list(group))) + key for key,group in groupby(seed))
			arr.append(current)
			get_sequence(arr, niter-1, current)
		return arr

	final_sequence = get_sequence(arr, niter, seed)
	str_sequence = '\r\n'.join(final_sequence)
	return str_sequence

def serve_request(conn):
	# receive request from client
	req = conn.recv(1024).decode('ascii')
	print(req)
	# control request
	m = re.match(r'^([0-9]),([0-9]+)\\r\\n$', req)
	if not m:
		# wrong request
		conn.sendall('+ERR\r\n'.encode('ascii'))
	else:
		# right request
		# get parameters from request
		seed = m.group(1)
		niter = int(m.group(2))
		# send response line
		msg = '+OK '+ str(niter) +' iterations on seed '+ seed +'\r\n'
		conn.sendall(msg.encode('ascii'))
		# process request
		reply = look_and_say(seed, niter)
		# send reply
		conn.sendall(reply.encode('ascii'))
		#print(reply)

		time.sleep(1)
		conn.close()

"""
The BSD server creates a socket, uses bind to attach that socket to a port,
and configures it as a listening socket.
This allows the server to receive incoming connection requests.
Afterwards, accept is called, which will block the socket,
until an incoming connection request is received
"""
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	# AF_INET means using IPv4
	# SOCK_STREAM means using TCP
	# use SOCK_DGRAM for UDP

	# BINDING
	s.bind((HOST, PORT))
	# LISTEN
	s.listen()
	# LOOP
	while True:
		# ACCEPT
		conn, addr = s.accept()
		# fork, generating child
		pid = os.fork()
		# parent with pid > 0
		if pid > 0:
			"""
			print("I am parent process:")
			print("Process ID:", os.getpid())
			print("Child's process ID:", pid)
			"""
			conn.close()

		# child with pid = 0
		else:
			"""
			print("\nI am child process:")
			print("Process ID:", os.getpid())
			print("Parent's process ID:", os.getppid())
			"""

			# serve client request
			serve_request(conn)
			
			sys.exit()



