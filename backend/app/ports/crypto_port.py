from abc import ABC, abstractmethod

class CryptoPort(ABC):
    """
    Puerto (Interfaz) criptográfico siguiendo la Arquitectura Limpia.
    Define los contratos que cualquier adaptador de encriptación debe cumplir
    para ser utilizado por los casos de uso, desacoplando así la lógica de negocio
    de la librería criptográfica específica.
    """
    
    @abstractmethod
    def encrypt(self, plain_text: str, password: str) -> str:
        """
        Encripta un texto plano utilizando una contraseña.
        
        Args:
            plain_text (str): El mensaje original.
            password (str): La contraseña secreta del usuario.
            
        Returns:
            str: El payload resultante encriptado (idealmente codificado para URLs).
        """
        pass

    @abstractmethod
    def decrypt(self, cipher_text: str, password: str) -> str:
        """
        Desencripta un payload cifrado utilizando una contraseña.
        
        Args:
            cipher_text (str): El payload cifrado.
            password (str): La contraseña secreta ingresada para intentar descifrar.
            
        Returns:
            str: El mensaje original en texto plano.
            
        Raises:
            ValueError: Si la contraseña es incorrecta o el payload es inválido.
        """
        pass
