import base64
class Encryptor:
    def encryption_using_xor(self,data,key):
        encrypted_bytes = ''
        try:
            for i, word in enumerate(data):
                    encrypted_bytes += chr(ord(word) ^ key)
            return base64.b64encode(encrypted_bytes).decode("utf-8")
        except:
             return encrypted_bytes
        