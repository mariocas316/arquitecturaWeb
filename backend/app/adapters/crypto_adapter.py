import base64
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidTag
from app.ports.crypto_port import CryptoPort

class CryptoAdapter(CryptoPort):
    def _derive_key(self, password: str, salt: bytes) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=390000,
        )
        return kdf.derive(password.encode('utf-8'))

    def encrypt(self, plain_text: str, password: str) -> str:
        salt = os.urandom(16)
        nonce = os.urandom(12)
        key = self._derive_key(password, salt)
        aesgcm = AESGCM(key)
        ciphertext = aesgcm.encrypt(nonce, plain_text.encode('utf-8'), None)
        
        # Combine salt, nonce, and ciphertext
        combined = salt + nonce + ciphertext
        return base64.urlsafe_b64encode(combined).decode('utf-8')

    def decrypt(self, payload: str, password: str) -> str:
        try:
            combined = base64.urlsafe_b64decode(payload.encode('utf-8'))
            if len(combined) < 28:
                raise ValueError("Payload inválido")
            
            salt = combined[:16]
            nonce = combined[16:28]
            ciphertext = combined[28:]
            
            key = self._derive_key(password, salt)
            aesgcm = AESGCM(key)
            plain_text = aesgcm.decrypt(nonce, ciphertext, None)
            return plain_text.decode('utf-8')
        except InvalidTag:
            raise ValueError("Contraseña incorrecta o mensaje corrupto")
        except Exception as e:
            raise ValueError("Error al desencriptar el mensaje")
