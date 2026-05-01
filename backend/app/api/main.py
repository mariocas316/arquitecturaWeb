from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.domain.models import MessageRequest, EncryptedMessageResponse, DecryptRequest, DecryptedMessageResponse
from app.adapters.crypto_adapter import CryptoAdapter
from app.use_cases.encrypt_message import EncryptMessageUseCase
from app.use_cases.decrypt_message import DecryptMessageUseCase

app = FastAPI(title="API de Mensajes Encriptados")

# Configurar CORS para permitir solicitudes del frontend (Reflex o React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar dependencias (Clean Architecture)
crypto_adapter = CryptoAdapter()
encrypt_use_case = EncryptMessageUseCase(crypto_adapter)
decrypt_use_case = DecryptMessageUseCase(crypto_adapter)

@app.post("/api/encrypt", response_model=EncryptedMessageResponse)
def encrypt_message(request: MessageRequest):
    try:
        payload = encrypt_use_case.execute(request.message, request.password)
        return EncryptedMessageResponse(url_payload=payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/decrypt", response_model=DecryptedMessageResponse)
def decrypt_message(request: DecryptRequest):
    try:
        message = decrypt_use_case.execute(request.url_payload, request.password)
        return DecryptedMessageResponse(message=message)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
