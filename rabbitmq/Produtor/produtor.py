import sys
import zmq
from random import *
import time
import threading

def escolhendo_msg():
	msg = ["Ola", "Tudo bem", "Bom dia", "Como vai", "Hello", 
	"Boa noite", "Boa tarde", "Tchau", "Oi", "Eai", "Opa", "Falou"]
	
	i = randint(0, 11)

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

	time.sleep(3)
	print("Enviando a msg do produtor...")
	

	send_msg = str.encode(f"{topico} {mensagem}")
	s.send(send_msg)
	msg = s.recv()
	result = bytes.decode(msg)


def main():
	mensagem_escolhida = escolhendo_msg()
	print("Mensagem escolhida: ",mensagem_escolhida)
	topico_escolhido = escolhendo_topico()
	print("Topico escolhido", topico_escolhido)
	enviando_mensagem(topico_escolhido, mensagem_escolhida)


if __name__ == '__main__':

	while True:
		time.sleep(5)
		thread = threading.Thread(target=main)
		thread.start()
		thread.join()

