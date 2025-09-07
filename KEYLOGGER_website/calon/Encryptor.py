#התוכנה שמצפינה
class Encryptor1:
    def __init__(self):
        pass
    def encryption_using_xor(self,data,key):
        encrypted_text = ''
        try:
            for i, word in enumerate(data):
                if word == '[' or word == ']':
                    continue
                else:    
                    encrypted_text += chr(ord(word) ^ key)
            # print (encrypted_text)    
            return self.encrypted_text
        except:
             return encrypted_text
        