#התוכנה שמצפינה
class Encryptor:
    def encryption_using_xor(data,key):
        encrypted_text = ''
        try:
            for i, word in enumerate(data):
                if word == '[' or word == ']':
                    continue
                else:    
                    encrypted_text += chr(ord(word) ^ key)
            print (encrypted_text)    
            return encrypted_text
        except:
             return encrypted_text