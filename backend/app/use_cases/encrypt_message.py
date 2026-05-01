from app.ports.crypto_port import CryptoPort

class EncryptMessageUseCase:
    """
    Caso de uso para la encriptación de mensajes.
    Contiene las reglas de negocio aisladas asociadas a la acción de encriptar.
    """
    
    def __init__(self, crypto_port: CryptoPort):
        """
        Inicializa el caso de uso inyectando la dependencia de criptografía.
        
        Args:
            crypto_port (CryptoPort): Interfaz para el servicio de encriptación.
        """
        self.crypto_port = crypto_port

    def execute(self, message: str, password: str) -> str:
        """
        Ejecuta la regla de negocio para encriptar un mensaje.
        Verifica que los datos de entrada sean válidos antes de proceder.
        
        Args:
            message (str): El mensaje a encriptar.
            password (str): Contraseña del usuario.
            
        Returns:
            str: El texto cifrado.
            
        Raises:
            ValueError: Si el mensaje o la contraseña están vacíos.
        """
        if not message or not password:
            raise ValueError("El mensaje y la contraseña no pueden estar vacíos")
        return self.crypto_port.encrypt(message, password)
