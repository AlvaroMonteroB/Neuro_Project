import socket
import threading


class unity_conector:
    def __init__(self) -> None:
        self.server_socket=socket.socket(
         family=socket.AF_INET, type=socket.SOCK_STREAM, proto=socket.IPPROTO_TCP
    )
        self.server_socket.connect('127.0.0.1',5052)
        self.data_tuple
     
    @staticmethod    
    def _init_thread(target,args=()):
        threading.Thread(target=target,args=args).start()
        
    def transfer_data(self,data_tuple):
        self.server_socket.sendto(str(data_tuple[0]+data_tuple[1]))#Enviar concentracion y mano
        