import sys
import zmq
from random import *
import time
import threading

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

def main(i):
	mensagem_escolhida = escolhendo_msg()
	print(mensagem_escolhida)
	topico_escolhido = escolhendo_topico()
	print(topico_escolhido)
	enviando_mensagem(topico_escolhido, mensagem_escolhida)
	#time.sleep(1)
	#a = input("diga meu fih")

if __name__ == '__main__':
	#threads = []
	while True:
		i = 0
		time.sleep(5)
		thread = threading.Thread(target=main, args=(i,))
		thread.start()
		thread.join()
		i += 1

	#main()