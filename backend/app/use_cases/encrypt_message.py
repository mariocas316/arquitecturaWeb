from app.ports.crypto_port import CryptoPort

class EncryptMessageUseCase:
    def __init__(self, crypto_port: CryptoPort):
        self.crypto_port = crypto_port

    def execute(self, message: str, password: str) -> str:
        if not message or not password:
            raise ValueError("El mensaje y la contraseña no pueden estar vacíos")
        return self.crypto_port.encrypt(message, password)
