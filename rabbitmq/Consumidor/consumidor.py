import threading
import time

import zmq

def receber(porta: int):
    print("Iniciando conexão com o Trocador")
    context = zmq.Context()
    s = context.socket(zmq.REP)
    PORTA = porta
    HOST = '192.168.18.6'
    p = f"tcp://{HOST}:{PORTA}"
    #s.bind("tcp://192.168.18.6:{PORTA}")
    s.bind(p)
    

    print("Conexão realizada")

    #time.sleep(3)
    print("Recebendo a msg...")
    msg = s.recv()
    decoded = bytes.decode(msg)

    print("Mensagem recebida: ", decoded)  
    s.send(str.encode("Mensagem recebida"))
if __name__ == '__main__':
    porta = input("Digite a porta que vc usara...")
    while True:
        time.sleep(1)
        print("Aguardando msg")
        thread_receber = threading.Thread(target=receber, args=(porta,))
        thread_receber.start()
        thread_receber.join()
