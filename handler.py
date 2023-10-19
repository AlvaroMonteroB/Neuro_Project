from rx.subject import Subject 
import threading
import numpy as np
import matplotlib.pyplot as plt
class Data_handler:
    def __init__(self) -> None:
        self.raw_data=[]
        self.numpy_tuple=np.array
    def handler(self,data):
        self.raw_data.append(data)
        
        
    def call_plot(self):
        plt.plot(self.numpy_tuple)
        plt.show()
        
        
        
    @staticmethod    
    def _init_thread(target,args=()):
        threading.Thread(target=target, args=args).start()