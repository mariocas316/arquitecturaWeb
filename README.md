# Secret Share 🔒

Aplicación web diseñada para intercambiar mensajes encriptados de forma segura mediante un enlace. La característica principal de esta aplicación es su **Almacenamiento Efímero Segurizado**; los mensajes se guardan cifrados en base de datos usando un ORM y se destruyen al ser leídos, garantizando la privacidad.

---

## 🛠️ Frameworks Seleccionados

1. **Backend**: [FastAPI](https://fastapi.tiangolo.com/) y **SQLAlchemy (ORM)**
   - Seleccionados por su altísimo rendimiento, validación estricta de datos (Pydantic), y capacidades potentes de mapeo objeto-relacional para gestionar el CRUD completo (Create, Read, Update, Delete) en base de datos SQLite de forma segura.
2. **Frontend**: [Reflex](https://reflex.dev/)
   - Seleccionado por ser un framework *Full-Stack* basado 100% en Python, lo que permite desarrollar interfaces de usuario reactivas complejas sin necesidad de escribir Javascript, facilitando la unificación del lenguaje en todo el proyecto.

---

## 🏗️ Arquitectura de las Aplicaciones

### 1. Backend: Clean Architecture (Arquitectura Limpia)
El backend está estructurado bajo los principios de Clean Architecture para lograr un desacoplamiento total entre la lógica de negocio, las herramientas criptográficas, el ORM y el framework web.

Sus capas (ubicadas en `backend/app/`) son:
- **`domain/` (Dominio):** Contiene las entidades principales y contratos de datos utilizando modelos de Pydantic.
- **`ports/` (Puertos):** Interfaces abstractas (Ej. `CryptoPort`) que definen cómo se debe comportar el servicio criptográfico.
- **`adapters/` (Adaptadores):** Implementaciones concretas. Aquí vive `CryptoAdapter`, que utiliza la librería `cryptography` (AES-GCM y PBKDF2HMAC) para encriptar los datos antes de persistirlos.
- **`use_cases/` (Casos de Uso):** Contienen la lógica pura del negocio (`EncryptMessageUseCase` y `DecryptMessageUseCase`).
- **`infrastructure/` (Infraestructura):** Integración del **ORM SQLAlchemy** (`database.py`, `models.py`) donde persiste de forma efímera los datos.
- **`api/` (API):** El marco de FastAPI (`main.py`) exponiendo un **CRUD completo** con manejo de errores:
  - `POST /api/messages`: Crea el mensaje.
  - `GET /api/messages/{id}`: Lee el mensaje (y lo autodestruye).
  - `PUT /api/messages/{id}`: Actualiza un mensaje existente.
  - `DELETE /api/messages/{id}`: Borra manualmente un mensaje.

### 2. Frontend: Arquitectura Modular de Reflex
El frontend está estructurado siguiendo las recomendaciones oficiales de escalabilidad de Reflex:
- **`state.py`:** Administra el estado global y las llamadas asíncronas HTTP (vía `httpx`) que se comunican con el CRUD del Backend.
- **`styles.py`:** Centraliza los diccionarios de diseño y colores globales.
- **`pages/`:** Contiene la interfaz de usuario pura, desacoplada en diferentes vistas (`index.py` y `read.py`).
- **`frontend.py`:** Actúa únicamente como enrutador principal para inicializar la aplicación.

---

## 🧪 Pruebas (Testing)
El backend cuenta con pruebas unitarias (`backend/tests/test_api.py`) utilizando `pytest` y `TestClient` que verifican de manera exhaustiva **todos los métodos HTTP del CRUD (GET, POST, PUT, y DELETE)** y comprueban los escenarios de error.

---

## 🚀 Cómo ejecutar el proyecto en tu entorno local

### Prerrequisitos del sistema
```bash
sudo apt update
sudo apt install python3-pip python3.12-venv
```

### Paso 1: Levantar el Backend (FastAPI)
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn cryptography pydantic pydantic-settings sqlalchemy
uvicorn app.api.main:app --reload
```
*El API quedará disponible en `http://localhost:8000`.*

### Paso 2: Levantar el Frontend (Reflex)
Abre una **nueva terminal**:
```bash
cd frontend
python3 -m venv venv
source venv/bin/activate
pip install reflex httpx
reflex init
reflex run
```
*El Frontend quedará disponible en `http://localhost:3000`.*
