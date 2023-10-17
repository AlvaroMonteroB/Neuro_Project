from rx.subject import Subject 
import connection
class Data_handler:
    def __init__(self) -> None:
        self.raw_data=[]
    def handler(self,data):
        self.raw_data.append(data)
    