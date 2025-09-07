from abc import ABC, abstractmethod

class IWriter(ABC):
    @abstractmethod
    def send_data(self, data: str, machine_name: str):
        for i in data:
            text += i
        with open('text','a') as file:
            file.write(text)
        