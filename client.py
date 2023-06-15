#!/usr/bin/env python3

import socket
import sys
import json
import re

# Standard loopback interface address (localhost)
HOST = '127.0.0.1'
#HOST = sys.argv[1] # let user choose host, 'localhost'=127.0.0.1
# Port to listen on (non-privileged ports are > 1023)
PORT = 8080
#PORT = int(sys.argv[2]) # let user choose port

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

	# CONNECTION: contact server in listen
	s.connect((HOST, PORT))

	# params
	user_entry = input('Enter <IP_address>/<netmask_len>: ')
	
	m = re.match(r'^(.+?)\/(.+)$', user_entry)
	if not m:
		#wrong entry
		print('Wrong entry')
		s.close()
		exit()
	else:
		IP_address = user_entry.split('/')[0]
		netmask_len = user_entry.split('/')[1]
		

	# controls on params
	m = re.match(r'^((?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?).){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$', IP_address)
	if not m:
		#not an ip
		print(f'ERR: {IP_address} is not an ip address')
		s.close()
		exit()
	else:
		#correct ip
		print(f'OK: {IP_address} is an ip address')


	m = re.match(r'^(?:[0-9]|[1-2][0-9]|3[0-2])$', netmask_len)
	if not m:
		#not a netmask
		print(f'ERR: {netmask_len} is not a netmask')
		s.close()
		exit()
	else:
		#correct netmask
		print(f'OK: {netmask_len} is a netmask')


	# params ok
	# request for server
	request_dict = {"netid": str(IP_address), "netmaskCIDR": str(netmask_len)}
	request_json = json.dumps(request_dict)

	# print for debug
	#print(request_dict)

	s.sendall(request_json.encode('ascii'))

	# reply from server
	reply_json = s.recv(1024).decode('ascii')
	reply_dict = json.loads(reply_json)

	print(reply_dict)

	# close socket
	s.close()

