from pydantic import BaseModel

class MessageRequest(BaseModel):
    message: str
    password: str

class EncryptedMessageResponse(BaseModel):
    url_payload: str

class DecryptRequest(BaseModel):
    url_payload: str
    password: str

class DecryptedMessageResponse(BaseModel):
    message: str
