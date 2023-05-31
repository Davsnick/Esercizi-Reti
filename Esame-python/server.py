#!/usr/bin/env python3

	#SERVER
import socket
import sys
import time
import os
from itertools import *

HOST = '127.0.0.1'	#Standard loopback interface address (localhost)
PORT = 8080	#Port to listen on (non-privileged ports are > 1023)

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
			get_sequence(arr, niter, current)
		return arr

	final_sequence = get_sequence(arr, niter-1, seed)
	return final_sequence


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

	#binding: operazione per fornire un numero di porta al client
	s.bind((HOST, PORT))

	#listen: operazione per preparare il socket a ricevere una connessione
	s.listen()

	#ciclo infinito
	while True:

		#accept: accettazione della nuova richiesta di connessione
		conn, addr = s.accept()

		#fork per generare figli
		pid = os.fork()

		#padre con pid>0
		if pid > 0:
			print("I am parent process:")
			print("Process ID:", os.getpid())
			print("Child's process ID:", pid)
			conn.close()


		#figlio con pid=0
		else:
			print("\nI am child process:")
			print("Process ID:", os.getpid())
			print("Parent's process ID:", os.getppid())

			#print('Connected by', addr)
			data = conn.recv(1024)
			data = data.decode('utf-8')
			seed, niter = data.split(",")
			print('seed=' + seed + ', niter=' + niter)
			sequence = look_and_say(seed, niter)
			print('Here is the message: %s'% sequence.decode('utf-8'))
			#conn.sendall(message.encode('utf-8'))
			# socket must be closed by client! sleep for 1 second to wait for the client
			time.sleep(1)
	# otherwise socket goes to TIME_WAIT!


