from abc import ABC, abstractmethod

class CryptoPort(ABC):
    @abstractmethod
    def encrypt(self, plain_text: str, password: str) -> str:
        pass

    @abstractmethod
    def decrypt(self, cipher_text: str, password: str) -> str:
        pass
