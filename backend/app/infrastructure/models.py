from sqlalchemy import Column, String
from .database import Base
import uuid

class MessageDB(Base):
    """
    Modelo ORM de SQLAlchemy para la tabla 'messages'.
    Representa cómo se estructura un mensaje encriptado en la base de datos.
    
    Attributes:
        id (String): Identificador único universal (UUID) que actúa como Primary Key.
        encrypted_payload (String): Cadena que contiene el mensaje totalmente cifrado.
    """
    __tablename__ = "messages"
    
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    encrypted_payload = Column(String, nullable=False)
