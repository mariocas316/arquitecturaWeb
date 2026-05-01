from pydantic import BaseModel

class MessageRequest(BaseModel):
    """
    Modelo Pydantic para la solicitud de creación o actualización de un mensaje.
    
    Attributes:
        message (str): El texto del mensaje que se desea encriptar.
        password (str): La contraseña provista por el usuario para cifrar el mensaje.
    """
    message: str
    password: str

class EncryptedMessageResponse(BaseModel):
    """
    Modelo Pydantic obsoleto para URLs sin persistencia (mantenido por compatibilidad).
    
    Attributes:
        url_payload (str): El paquete cifrado codificado en base64.
    """
    url_payload: str

class DecryptRequest(BaseModel):
    """
    Modelo Pydantic para la solicitud de desencriptación de un mensaje sin persistencia.
    
    Attributes:
        url_payload (str): El payload encriptado proveniente de la URL.
        password (str): La contraseña para intentar desencriptar.
    """
    url_payload: str
    password: str

class DecryptedMessageResponse(BaseModel):
    """
    Modelo Pydantic para responder con el mensaje ya desencriptado en texto plano.
    
    Attributes:
        message (str): El mensaje original descifrado.
    """
    message: str
