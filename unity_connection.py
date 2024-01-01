import socket
import threading


class unity_conector:
    def __init__(self) -> None:
        self.server_socket=socket.socket(
         family=socket.AF_INET, type=socket.SOCK_STREAM, proto=socket.IPPROTO_TCP
    )
        self.server_socket.connect('127.0.0.1',5052)
        self.cons_data=[]
        
     
    @staticmethod    
    def _init_thread(target,args=()):#Inicia hilo de procesamiento
        threading.Thread(target=target,args=args).start()
        
    def add_data(self,data):
        self.cons_data.append(data)
        self._init_thread(target=self.transfer_data)
        
    def transfer_data(self,data_tuple):
        self.server_socket.sendto(str(self.cons_data))#Enviar concentracion y mano
        