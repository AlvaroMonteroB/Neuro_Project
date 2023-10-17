import numpy as np
import threading
import connection as cn
from time import sleep
from rx.internal import DisposedException
from rx.subject import Subject
from rx.operators import take_until_with_time


class Processor():
    def __init__(self) -> None:
        self.live_recording=False
        self.data_res=250
        self.blink_threshold=50000000
        self.recorded_data=[]
        self.is_recording=False
        self.is_open=True
        self.sample_freq=512
        self.batch_mode=False
        self.processed_data=[]
        
        #susbscriptions
        self.subscriptions=[]
        
        #observadores
        self.data=Subject()
        self.subscriptions.append(self.data)
        
        #ocultos
        self.raw_data_batch=[]
        
    def _init_thread(target,args=()):
        threading.Thread(target=target,args=args)
        
        
    def add_data(self,raw_data):
        if not self.batch_mode:
            self.raw_data_batch.append(raw_data)
            if len(self.raw_data_batch)>=self.data_res and self.is_open:
                self._init_thread(target=self._fft)#Aqui llamamos a la fft para descomponer los dstos
                
    def _fft(self):
        temp_data_batch=self.raw_data_batch.copy
        self.raw_data_batch=[]
        batch_size=len(temp_data_batch)
        if len(batch_size)!=0 and (
                self.blink_threshold > np.amax(temp_data_batch) or -self.blink_threshold < np.amin(temp_data_batch)):
            x_fft=np.fft.rfftfreq(batch_size,2*(1/self.sample_freq))
        slice_size = round(len(list(filter(lambda x: x < 50, x_fft))), -1)
        x_fft = x_fft[:slice_size]
        y_fft = np.absolute(np.real(np.fft.rfft(temp_data_batch)))[:slice_size]
        self.processed_data = np.array([x_fft, y_fft])[1]
        self.data.on_next(self.processed_data)            
        
        
    def close(self):
        self.is_open=True
        sleep(1.5)
        for subs in self.subscriptions:
            try:
                subs.dispose()
            except DisposedException:
                pass
            print("Process closed")
        