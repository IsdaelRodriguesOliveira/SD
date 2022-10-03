



import time
import zmq
import json
import threading
import traceback

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

    #s.bind("tcp://192.168.18.6:8001")
    s.bind_to_random_port('tcp://192.168.18.6', min_port=8001, max_port=8002, max_tries=100)

    time.sleep(2)
    print("Recebendo a msg...")
    try:
        msg = s.recv(flags=1)
        decoded = bytes.decode(msg)

        print("Mensagem recebida: ")
        msg = json.dumps(decoded, indent = 4)
        topico = str(msg[1:7])
        msg = str(msg[8:-1])
        print("Topico da msg =", topico)
        print("MSG =", msg)
        adicionar_msg_lista(msg,topico)
        s.send(str.encode("Mensagem recebida"))

    except zmq.ZMQError as e:
        print("Sem conexao com o produtor")
        if e.errno == zmq.EAGAIN:
            pass # no message was ready (yet!)
        else:
            traceback.print_exc()

    #s.zmq_close()

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

def enviar_msg(porta: int, topico: str):
    PORT = porta
    HOST = '192.168.18.6'
    context = zmq.Context()
    s  = context.socket(zmq.REQ)
    p = f"tcp://{HOST}:{PORT}"
    s.connect(p)

    time.sleep(3)
    print("Enviando para o consumidor...")

    try:
        if topico == "fila_0":
            msg = fila_fila_0[0]
            send_msg = str.encode(f"{msg}")
            s.send(send_msg, flags=zmq.NOBLOCK)
            fila_fila_0.pop()
        elif topico == "fila_1":
            msg = fila_fila_1[0]
            send_msg = str.encode(f"{msg}")
            s.send(send_msg, flags=zmq.NOBLOCK)
            fila_fila_1.pop()
        elif topico == "fila_2":
            msg = fila_fila_2[0]
            send_msg = str.encode(f"{msg}")
            s.send(send_msg, flags=zmq.NOBLOCK)
            fila_fila_2.pop()
        elif topico == "fanout":
            msg = fila_fanout[0]
            send_msg = str.encode(f"{msg}")
            s.send(send_msg, flags=zmq.NOBLOCK)
            fila_fanout.pop()

        else:
            print("Topico de envio nao encontrado")
    #send_msg = str.encode(f"{topico}")
    #msg = s.recv(flags=zmq.NOBLOCK)
        msg = s.recv(flags=zmq.NOBLOCK)
        print("Mensagem enviada com sucesso")
    except zmq.ZMQError as e:
        print("Sem conexao do consumidor")
        if e.errno == zmq.EAGAIN:
            pass # no message was ready (yet!)
        else:
            traceback.print_exc()

def verifica_filas():
    porta = 8010
    if len(fila_fila_0) != 0:
        enviar_msg(porta, "fila_0")
    elif len(fila_fila_1) != 0 :
        enviar_msg(porta, "fila_1")
    elif len(fila_fila_2) != 0:
        enviar_msg(porta, "fila_2")
    elif len(fila_fanout) != 0:
        enviar_msg(porta, "fanout")
    else:
        print("Filas vazias")

if __name__ == '__main__':
    while True:
        #time.sleep(5)
        print("-------------------------------")
        print("Iniciando thread de recebimento, no Trocador")
        thread_receber = threading.Thread(target=receber)
        thread_receber.start()
        thread_receber.join()
        print("Thread de recebimento finalizada")
        print("-------------------------------")
        print("Iniciando thread de envio, no Trocador")
        fila_fanout.insert(0,"Como vai")
        thread_enviar = threading.Thread(target=verifica_filas)
        thread_enviar.start()
        thread_enviar.join(timeout=2)
        print("Thread de envio finalizada")
