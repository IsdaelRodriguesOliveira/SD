import time
from tokenize import String
import zmq
import sys
import json

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
    #s.send(str.encode("{:.2f}".format(result)))