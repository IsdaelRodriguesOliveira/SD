import threading
import time

import zmq

def receber():
    print("Iniciando conexão com o Trocador")
    context = zmq.Context()
    s = context.socket(zmq.REP)

    s.bind("tcp://192.168.18.6:8010")
    

    print("Conexão realizada")

    time.sleep(3)
    print("Recebendo a msg...")
    msg = s.recv()
    decoded = bytes.decode(msg)

    print("Mensagem recebida: ", decoded)  
    s.send(str.encode("Mensagem recebida"))
if __name__ == '__main__':
    while True:
        time.sleep(5)
        print("Aguardando msg")
        thread_receber = threading.Thread(target=receber)
        thread_receber.start()
        thread_receber.join()
