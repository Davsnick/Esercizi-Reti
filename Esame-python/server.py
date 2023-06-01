#!/usr/bin/env python3

	#SERVER
import socket
import sys
import time
import os
import re
from itertools import *

HOST = '127.0.0.1'	#Standard loopback interface address (localhost)
PORT = 8080	#Port to listen on (non-privileged ports are > 1023)

def control(seed, niter):
	if len(seed) != 1:
		print('seed troppo lungo')
		return 0
	if seed.isnumeric() == False:
		print('seed non numero')
		return 0
	if niter.isnumeric() == False:
		print('niter non numero')
		return 0
	return 1

def look_and_say(seed, niter):
	seed = str(seed)
	niter = int(niter)
	arr = [seed]

	def get_sequence(arr, niter, seed):
		if niter == 0:
			#print('esco')
			return arr
		else:
			#print('itero')
			current = ''.join(str(len(list(group))) + key for key,group in groupby(seed))
			arr.append(current)
			get_sequence(arr, niter-1, current)
		return arr

	final_sequence = get_sequence(arr, niter, seed)
	#print('ritorno')
	return final_sequence

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

	"""
	The BSD server creates a socket, uses bind to attach that socket to a port,
	and configures it as a listening socket.
	This allows the server to receive incoming connection requests.
	Afterwards, accept is called, which will block the socket,
	until an incoming connection request is received
	"""
	#binding
	s.bind((HOST, PORT))
	#listen
	s.listen()

	#loop
	while True:
		#accept
		conn, addr = s.accept()

		#fork, generating child
		pid = os.fork()

		#padre con pid>0
		if pid > 0:
			#print("I am parent process:")
			#print("Process ID:", os.getpid())
			#print("Child's process ID:", pid)
			conn.close()

		#figlio con pid=0
		else:
			#print("\nI am child process:")
			#print("Process ID:", os.getpid())
			#print("Parent's process ID:", os.getppid())

			#ricevo i dati da un client
			data = conn.recv(1024)
			data = data.decode('utf-8')
			seed, niter = data.split(",")
			niter = niter.split("/")[0]
			#print('seed=' + seed + ', niter=' + niter)
			
			#controllo che seed e niter siano corretti
			if control(seed, niter) == 0:
				print('- ERR')
			else:
				print('+OK '+ niter +' iterations on seed '+ seed +'/r/n')

				sequence = look_and_say(seed, niter)

				for line in sequence:
					print(str(int(line)) + '/r/n')
				
			# socket must be closed by client! sleep for 1 second to wait for the client
			time.sleep(1)
				
			sys.exit()



