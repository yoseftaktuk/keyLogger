from abc import ABC, abstractmethod

class Encryptor(ABC):
     @abstractmethod
     def encryption_using_xor(self,data,key):
          pass