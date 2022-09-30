import time
from tokenize import String
import zmq
import sys
import json
import threading

fila_fila_0 = []
fila_fila_1 = []
fila_fila_2 = []
fila_fanout = []

#QUANTITY_PORTS = sys.argv[1] or 1
#INITIAL_PORT = sys.argv[2] or 8000

def receber():
    print("Iniciando conexão")
    context = zmq.Context()
    s = context.socket(zmq.REP)
    PORT1 = 8001
    HOST = '192.0.0.130'
    p1 = f"tcp://*:5001" 

    s.bind("tcp://192.168.18.6:8001")

    print("Conexão realizada")

    time.sleep(3)
    print("Recebendo a msg...")
    msg = s.recv()
    decoded = bytes.decode(msg)

    print("Mensagem recebida: ", decoded)
    msg = json.dumps(decoded, indent = 4)
    topico = str(msg[1:7])
    msg = str(msg[8:-1])

    print("Topico da msg =", topico, len(topico))
    print("MSG =", msg, len(msg))
    
    s.send(str.encode("Mensagem recebida"))
    adicionar_msg_lista(msg,topico)

def adicionar_msg_lista(msg, topico):
    if topico == "fila_0":
        fila_fila_0.insert(0, str(msg))
        print("Adicionado a fila 0 ", fila_fila_0[0])
    elif  topico == "fila_1":
        fila_fila_1.insert(0, str(msg))
        print("Adicionado a fila 1 ", fila_fila_1[0])
    elif topico == "fila_2":
        fila_fila_2.insert(0, str(msg))
        print("Adicionado a fila 2 ", fila_fila_2[0])
    elif  topico == "fanout":
        fila_fanout.insert(0, str(msg))
        print("Adicionado a fila fanout ", fila_fanout[0])
    else: 
        print("Tópico da mensagem nao identificado Mensagem")

if __name__ == '__main__':
    while True:
        time.sleep(5)
        thread_receber = threading.Thread(target=receber)
        thread_receber.start()
        thread_receber.join()
