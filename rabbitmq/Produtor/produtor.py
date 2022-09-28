import sys
import zmq
from random import *
import time

"""	if sys.argv[1] == '1':
		port = 8001
	elif sys.argv[1] == '2':
		port = 8001
	else:
		print("Wrong arguments")
		exit()
"""
print("Iniciando conexão produtor")
port = 8001
HOST = '192.168.18.6'
context = zmq.Context()
s  = context.socket(zmq.REQ)
p = f"tcp://{HOST}:{port}"
s.connect(p)
print("Conexão realizada produtor")
while True:
	time.sleep(5)
	print("Mensagem do produtor")
	a = "{:.2f}".format(random()*10)
	b = "{:.2f}".format(random()*10)
	op = choice(["+", "*", "**"])

	send_msg = str.encode(f"{a} {op} {b}")
	s.send(send_msg)
	msg = s.recv()
	result = bytes.decode(msg)

	time.sleep(1)

	print (a, op, b, '=', result)