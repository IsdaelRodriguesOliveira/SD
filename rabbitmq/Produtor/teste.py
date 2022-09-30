import threading
import time
from random import *
import zmq

def start():
    op = 0

    while True:
        time.sleep(5)
        thread = Thread()
        thread.start()
        print("Digite -1 para parar :)")
        thread.stop()
        time.sleep(1)
    """while op != -1:
        t1 = Thread()
        t1.start()
        print("Digite -1 para parar :)")
        #op = int(input())
        t1.stop()
        time.sleep(1)
    print("saiu")"""

class Thread(threading.Thread):

    def __init__(self):
        super(Thread, self).__init__()
        self.kill = threading.Event()

    def run(self):
        # Enquanto a thread não estiver 'morta'
        self.main()
        """while not self.kill.is_set():
            print("Thread executando")
            time.sleep(1)"""

    def stop(self):
        # Mata a thread
        print("thread parando.")
        self.kill.set()
    def escolhendo_msg(self):
        msg = ["Ola", "Tudo bem", "Bom dia", "Como vai", "Hello", 
        "Boa noite", "Boa tarde", "Tchau", "Oi", "Eai", "Opa", "Falou"]
        
        i = randint(0, 11)
        #print(len(msg))
        return msg[i]
    def escolhendo_topico(self):
        topicos = ["fila_0", "fila_1", "fila_2", "fanout"]
        i = randint(0, 3)
        return topicos[i]

    def enviando_mensagem(self, topico, mensagem):
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

    def main(self):
        #while True:
        mensagem_escolhida = self.escolhendo_msg()
        print(mensagem_escolhida)
        topico_escolhido = self.escolhendo_topico()
        print(topico_escolhido)
        self.enviando_mensagem(topico_escolhido, mensagem_escolhida)

    

if __name__ == "__main__":
    start()