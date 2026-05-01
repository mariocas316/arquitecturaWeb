from app.ports.crypto_port import CryptoPort

class DecryptMessageUseCase:
    """
    Caso de uso para la desencriptación de mensajes.
    Aísla las reglas de negocio necesarias para descifrar de manera segura.
    """
    
    def __init__(self, crypto_port: CryptoPort):
        """
        Inicializa el caso de uso inyectando la dependencia de criptografía.
        
        Args:
            crypto_port (CryptoPort): Interfaz para el servicio de desencriptación.
        """
        self.crypto_port = crypto_port

    def execute(self, payload: str, password: str) -> str:
        """
        Ejecuta la regla de negocio para desencriptar un payload.
        Valida los parámetros de entrada antes de proceder.
        
        Args:
            payload (str): El texto cifrado (paquete base64).
            password (str): Contraseña suministrada por el usuario.
            
        Returns:
            str: El mensaje desencriptado.
            
        Raises:
            ValueError: Si los datos provistos están vacíos o el descifrado falla.
        """
        if not payload or not password:
            raise ValueError("El payload y la contraseña no pueden estar vacíos")
        return self.crypto_port.decrypt(payload, password)
