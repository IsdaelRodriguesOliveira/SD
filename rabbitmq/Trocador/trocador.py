import time
from tokenize import String
import zmq
import sys
import json

fila_fila_0 = []
fila_fila_1 = []
fila_fila_2 = []
fila_fanout = []

#QUANTITY_PORTS = sys.argv[1] or 1
#INITIAL_PORT = sys.argv[2] or 8000

print("Iniciando conexão trocador")
context = zmq.Context()
s = context.socket(zmq.REP)
PORT1 = 8001
HOST = '192.0.0.130'
p1 = f"tcp://*:5001" 
#p2 = f"tcp://{HOST}:{PORT2}"
s.bind("tcp://192.168.18.6:8001")
#s.bind(p2)
print("Conexão realizada trocador")
def receber():
    while True:
        time.sleep(5)
        print("Mensagem trocador")
        msg = s.recv()
        decoded = bytes.decode(msg)

        print("Received:", decoded)
        msg = json.dumps(decoded, indent = 4)
        a = str(msg[1:7])
        b = str(msg[8:-1])
        #b = str(b[7:-1])
        #decoded = str.split(decoded)
        #print("Received 2:", decoded)
        #b = str(decoded)
        #a = decoded[0]
        print("A =", a, len(a))
        print("B =", b, len(b))
        
        s.send(str.encode("Mensagem recebida"))
        adicionar_msg_lista(b,a)

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
    receber()