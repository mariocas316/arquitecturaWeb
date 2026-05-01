from sqlalchemy import Column, String
from .database import Base
import uuid

class MessageDB(Base):
    __tablename__ = "messages"
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    encrypted_payload = Column(String, nullable=False)
