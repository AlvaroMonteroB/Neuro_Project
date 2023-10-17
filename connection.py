import socket
import threading
import numpy as np
from json import loads
from time import sleep
import os
from rx.subject import Subject 
from rx.internal import DisposedException

class connector():
    def __init__(self) -> None:
        self.VERBOSE=False
        self.is_Open=True
        
        self.subscriptions=[]
        
        self.data=Subject()
        self.subscriptions.append(self.data)
        self.poor_signal_level=Subject()
        self.subscriptions.append(self.poor_signal_level)
        self.sampling_rate = Subject()
        self.subscriptions.append(self.sampling_rate)
        
      

        self.server_socket=socket.socket(
            family=socket.AF_INET, type=socket.SOCK_STREAM, proto=socket.IPPROTO_TCP)
        
        self._init_thread(target=self.generate_data)
        
        
        
    @staticmethod    
    def _init_thread(target,args=()):
        threading.Thread(target=target, args=args).start()
        
    def generate_sampling_rate(self):
        while self.is_Open:
            self._sampling_rate_counter = 0
            sleep(1)
            self.sampling_rate.on_next(self._sampling_rate_counter)
            
    def close(self):
        self.is_Open=False
        sleep(1.5)
        for subs in self.subscriptions:
            try:
                subs.dispose()
            except DisposedException:
                pass
        try:
            self.server_socket.close()
        finally:
            print("Connection closed")
                

    def generate_data(self):
        host='127.0.0.1'
        port=13854 #Puerto de thinkgear connector
        try:
            self.server_socket.connect(('127.0.0.1', 13854))
            self.server_socket.sendall(bytes('{"enableRawOutput":true,"format":"Json"}'.encode('ascii')))
            self._init_thread(target=self.generate_sampling_rate)

            

            print(f"Servidor escuchado en {host}:{port}")

            while self.is_Open:
                raw_bytes=self.server_socket.recv(1000)
                data_set = (str(raw_bytes)[2:-3].split(r'\r'))
                for data in data_set:
                    self.sampling_rate_counter=+1
                    try:
                        json_data=loads(data)
                        try:
                            temp_data=json_data['rawEeg']
                            
                            self.data.on_next(temp_data)#Aqui se guardan los datos crudos
                        except:
                            if len(json_data)>3:
                                self.poor_signal_level.on_next(json_data['eSense']['poorSignalLevel'])
                            else:
                                self.poor_signal_level.on_next(json_data['poorSignalLevel'])    
                    except:
                        continue
                if self.poor_signal_level==200 and self.VERBOSE:
                    print("Poor signal connection")
        except:
            self.close()
                


        self.server_socket.close()
        
    

