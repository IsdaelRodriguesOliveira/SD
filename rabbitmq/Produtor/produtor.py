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
def escolhendo_msg():
	msg = ["Ola", "Tudo bem", "Bom dia", "Como vai", "Hello", 
	"Boa noite", "Boa tarde", "Tchau", "Oi", "Eai", "Opa", "Falou"]
	
	i = randint(0, 11)
	#print(len(msg))
	return msg[i]
def escolhendo_topico():
	topicos = ["fila_0", "fila_1", "fila_2", "fanout"]
	i = randint(0, 3)
	return topicos[i]

def enviando_mensagem(topico, mensagem):
	print("Iniciando conexão produtor")
	port = 8001
	HOST = '192.168.18.6'
	context = zmq.Context()
	s  = context.socket(zmq.REQ)
	p = f"tcp://{HOST}:{port}"
	s.connect(p)
	print("Conexão realizada produtor")

	time.sleep(5)
	print("Mensagem do produtor")
	

	send_msg = str.encode(f"{topico} {mensagem}")
	s.send(send_msg)
	msg = s.recv()
	result = bytes.decode(msg)

	time.sleep(1)

	

def main():
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

if __name__ == '__main__':
	while True:
		mensagem_escolhida = escolhendo_msg()
		print(mensagem_escolhida)
		topico_escolhido = escolhendo_topico()
		print(topico_escolhido)
		enviando_mensagem(topico_escolhido, mensagem_escolhida)