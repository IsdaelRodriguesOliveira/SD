import time
import zmq
import json
import threading
import traceback

fila_fila_0 = ["Olaaa"]
fila_fila_1 = []
fila_fila_2 = []
fila_fanout = []


fila_fila_0 = threading.RLock()
fila_fila_1 = threading.RLock()
fila_fila_2 = threading.RLock()
fila_fanout = threading.RLock()

def adiciona(fila_atual):
    fila_atual.acquire()
    fila_atual.insert(0, input("Digite"))

if __name__ == '__main__':
    """thread_receber = threading.Thread(target=adiciona, args=(fila_fila_0,))
    thread_receber.start()
    thread_receber.join()"""
    print("Fila atual", fila_fila_0)
