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
    s.bind_to_random_port('tcp://192.168.18.6', min_port=8001, max_port=8002, max_tries=50)

    time.sleep(1)
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

def enviar_msg(fila_atual, porta: int):
    PORT = porta
    HOST = '192.168.18.6'
    context = zmq.Context()
    s  = context.socket(zmq.REQ)
    p = f"tcp://{HOST}:{PORT}"
    s.connect(p)

    time.sleep(3)
    print("...Enviando para o consumidor...")

    try:
       
        msg = fila_atual[0]
        send_msg = str.encode(f"{msg}")
        s.send(send_msg, flags=zmq.NOBLOCK)
        fila_atual.pop()
        
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

def verifica_filas(fila_atual):
    porta = 8010
    print(threading.current_thread)
    if len(fila_atual) != 0:
        enviar_msg(fila_atual, porta)
    else:
        print("Fila vazia")

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
        print("Iniciando thread de envio (fila 0), no Trocador")
        #fila_fanout.insert(0,"Como vai")
        thread_enviar_fila_0 = threading.Thread(target=verifica_filas, args=(fila_fila_0,))
        thread_enviar_fila_0.start()
        thread_enviar_fila_0.join(timeout=2)
        print("Finalizando thread de envio (fila 0), no Trocador")
        print("Iniciando thread de envio (fila 1), no Trocador")
        thread_enviar_fila_1 = threading.Thread(target=verifica_filas,args=(fila_fila_1,))
        thread_enviar_fila_1.start()
        thread_enviar_fila_1.join(timeout=2)
        print("Finalizando thread de envio (fila 1), no Trocador")
        print("Iniciando thread de envio (fila 2), no Trocador")
        thread_enviar_fila_2 = threading.Thread(target=verifica_filas, args=(fila_fila_2,))
        thread_enviar_fila_2.start()
        thread_enviar_fila_2.join(timeout=2)
        print("Finalizando thread de envio (fila 2), no Trocador")
        print("Iniciando thread de envio (fila fanout), no Trocador")
        thread_enviar_fila_fanout = threading.Thread(target=verifica_filas, args=(fila_fanout,))
        thread_enviar_fila_fanout.start()
        thread_enviar_fila_fanout.join(timeout=2)
        print("Finalizando thread de envio (fila fanout), no Trocador")
        print("Thread de envio finalizada")