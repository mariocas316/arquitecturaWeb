from app.ports.crypto_port import CryptoPort

class DecryptMessageUseCase:
    def __init__(self, crypto_port: CryptoPort):
        self.crypto_port = crypto_port

    def execute(self, payload: str, password: str) -> str:
        if not payload or not password:
            raise ValueError("El payload y la contraseña no pueden estar vacíos")
        return self.crypto_port.decrypt(payload, password)
