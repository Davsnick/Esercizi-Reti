#!/usr/bin/env python3

import socket
import sys
import json
import ipaddress
import time
import os
import re

# Standard loopback interface address (localhost)
HOST = '127.0.0.1'
#HOST = sys.argv[1] # let user choose host, 'localhost'=127.0.0.1
# Port to listen on (non-privileged ports are > 1023)
PORT = 8080
#PORT = int(sys.argv[2]) # let user choose port

def validate(IP_address, netmask_len):
	try:
	        # Validate network ID
		network = ipaddress.IPv4Network(IP_address + '/' + netmask_len, strict=False)
		if network.network_address != ipaddress.IPv4Address(IP_address):
			return False
        
		return True
	except (ipaddress.AddressValueError, ValueError):
		return False

def get_min_max(IP_address, netmask_len):
	try:
	        # Calculate network ID and netmask
		network = ipaddress.IPv4Network(IP_address + '/' + netmask_len, strict=False)
        
	        # Calculate minimum and maximum IP addresses
		min_ip = network.network_address
		max_ip = network.broadcast_address
        
		return str(min_ip), str(max_ip)

	except (ipaddress.AddressValueError, ValueError) as e:
		return None, None

def serve_request(conn):
	# receive request from client
	request_json = conn.recv(1024).decode('ascii')
	# print for debug	
	#print(request_json)

	request_dict = json.loads(request_json)
	IP_address = request_dict["netid"]
	netmask_len = request_dict["netmaskCIDR"]
	
	# control request
	if validate(IP_address, netmask_len):
		# calc IPmin and IPmax
		IPmin, IPmax = get_min_max(IP_address, netmask_len)
		reply_dict = {"status": "OK", "IPmin": IPmin, "IPmax": IPmax}
	else:
		# invalid ip
		reply_dict = {"status": "ERROR"}

	# send reply
	reply_json = json.dumps(reply_dict)
	conn.sendall(reply_json.encode('ascii'))
	# print for debug
	#print(reply)

	# sleep for 1 second to wait the client to close the socket
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
			# close parent process side socket
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
			# close child process, parent process still running
			sys.exit()



