import base64
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidTag
from app.ports.crypto_port import CryptoPort

class CryptoAdapter(CryptoPort):
    """
    Adaptador criptográfico que implementa la interfaz CryptoPort.
    Utiliza el estándar de grado militar AES-GCM para encriptación autenticada,
    y PBKDF2HMAC para derivar una llave fuerte a partir de la contraseña del usuario.
    """
    
    def _derive_key(self, password: str, salt: bytes) -> bytes:
        """
        Deriva una llave criptográfica segura de 32 bytes a partir de una contraseña.
        
        Args:
            password (str): La contraseña en texto plano.
            salt (bytes): Un valor aleatorio (salt) para frustrar ataques de diccionario.
            
        Returns:
            bytes: La llave de 32 bytes generada.
        """
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=390000,
        )
        return kdf.derive(password.encode('utf-8'))

    def encrypt(self, plain_text: str, password: str) -> str:
        """
        Encripta el texto utilizando AES-GCM. Genera un Salt y un Nonce aleatorios.
        
        Args:
            plain_text (str): El texto a encriptar.
            password (str): La contraseña de encriptación.
            
        Returns:
            str: Cadena en Base64 URL-safe que contiene [salt + nonce + ciphertext].
        """
        salt = os.urandom(16)
        nonce = os.urandom(12)
        key = self._derive_key(password, salt)
        aesgcm = AESGCM(key)
        ciphertext = aesgcm.encrypt(nonce, plain_text.encode('utf-8'), None)
        
        # Se combinan los vectores de inicialización junto con el texto cifrado
        combined = salt + nonce + ciphertext
        return base64.urlsafe_b64encode(combined).decode('utf-8')

    def decrypt(self, payload: str, password: str) -> str:
        """
        Desencripta el payload cifrado extrayendo el Salt y el Nonce originales.
        
        Args:
            payload (str): Cadena en Base64 URL-safe proveniente de la encriptación.
            password (str): Contraseña para intentar la desencriptación.
            
        Returns:
            str: El mensaje desencriptado.
            
        Raises:
            ValueError: Si la contraseña es incorrecta o los datos están corruptos.
        """
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
