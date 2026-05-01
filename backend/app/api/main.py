from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.domain.models import MessageRequest
from app.adapters.crypto_adapter import CryptoAdapter
from app.use_cases.encrypt_message import EncryptMessageUseCase
from app.use_cases.decrypt_message import DecryptMessageUseCase
from app.infrastructure.database import engine, Base, get_db
from app.infrastructure.models import MessageDB
from pydantic import BaseModel
from typing import Optional

Base.metadata.create_all(bind=engine)

app = FastAPI(title="API CRUD Mensajes Encriptados")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

crypto_adapter = CryptoAdapter()
encrypt_use_case = EncryptMessageUseCase(crypto_adapter)
decrypt_use_case = DecryptMessageUseCase(crypto_adapter)

class MessageResponse(BaseModel):
    id: str
    message: Optional[str] = None

# CREATE (POST)
@app.post("/api/messages", response_model=MessageResponse)
def create_message(request: MessageRequest, db: Session = Depends(get_db)):
    try:
        payload = encrypt_use_case.execute(request.message, request.password)
        db_msg = MessageDB(encrypted_payload=payload)
        db.add(db_msg)
        db.commit()
        db.refresh(db_msg)
        return {"id": db_msg.id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# READ (GET)
@app.get("/api/messages/{msg_id}", response_model=MessageResponse)
def read_message(msg_id: str, password: str, db: Session = Depends(get_db)):
    db_msg = db.query(MessageDB).filter(MessageDB.id == msg_id).first()
    if not db_msg:
        raise HTTPException(status_code=404, detail="Mensaje no encontrado")
    
    try:
        message = decrypt_use_case.execute(db_msg.encrypted_payload, password)
        # Opcional: Borrar al leer para mantener la privacidad
        db.delete(db_msg)
        db.commit()
        return {"id": msg_id, "message": message}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# UPDATE (PUT)
@app.put("/api/messages/{msg_id}", response_model=MessageResponse)
def update_message(msg_id: str, request: MessageRequest, db: Session = Depends(get_db)):
    db_msg = db.query(MessageDB).filter(MessageDB.id == msg_id).first()
    if not db_msg:
        raise HTTPException(status_code=404, detail="Mensaje no encontrado")
    
    try:
        new_payload = encrypt_use_case.execute(request.message, request.password)
        db_msg.encrypted_payload = new_payload
        db.commit()
        return {"id": msg_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# DELETE (DELETE)
@app.delete("/api/messages/{msg_id}")
def delete_message(msg_id: str, db: Session = Depends(get_db)):
    db_msg = db.query(MessageDB).filter(MessageDB.id == msg_id).first()
    if not db_msg:
        raise HTTPException(status_code=404, detail="Mensaje no encontrado")
    
    db.delete(db_msg)
    db.commit()
    return {"status": "eliminado exitosamente"}
