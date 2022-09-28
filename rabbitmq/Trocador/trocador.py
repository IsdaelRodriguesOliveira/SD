import time
import zmq
import sys

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

    decoded = str.split(decoded)
    if len(decoded) == 3:
        a, operation, b = decoded
        a = float (a)
        b = float (b)
    else:
        operation = 'invalid'
	
    if (operation == '+'):
        result = a+b
    elif (operation == '*'):
        result = a*b
    elif (operation == '**'):
        result = a**b
    else:
        result = 'invalid input'
	
    s.send(str.encode("{:.2f}".format(result)))