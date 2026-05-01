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

**Para Linux (Zorin OS / Ubuntu):**

```bash
sudo apt update
sudo apt install python3-pip python3.12-venv
```

**Para Windows:**

Debes tener instalado Python 3.10 o superior. Si usas PowerShell, antes de activar entornos virtuales debes permitir la ejecución de scripts. Abre PowerShell como Administrador (o en tu terminal actual) y ejecuta por única vez:

```powershell
Set-ExecutionPolicy Unrestricted -Scope CurrentUser
```

### Paso 1: Levantar el Backend (FastAPI)

**En Linux (Zorin OS):**

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn cryptography pydantic pydantic-settings sqlalchemy
uvicorn app.api.main:app --reload
```

**En Windows (PowerShell):**

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install fastapi uvicorn cryptography pydantic pydantic-settings sqlalchemy
uvicorn app.api.main:app --reload
```

*El API quedará disponible en `http://localhost:8000`.*

### Paso 2: Levantar el Frontend (Reflex)

Abre una **nueva terminal**:

**En Linux (Zorin OS):**

```bash
cd frontend
python3 -m venv venv
source venv/bin/activate
pip install reflex httpx
reflex init
reflex run --backend-port 8001
```

**En Windows (PowerShell):**

```powershell
cd frontend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install reflex httpx
reflex init
reflex run --backend-port 8001
```

*El Frontend quedará disponible en `http://localhost:3000`.*

---

## 🐳 Ejecución con Docker (Recomendado)

Si prefieres no instalar dependencias de Python localmente y evitar problemas de configuración, puedes levantar todo el proyecto (Backend y Frontend) usando Docker Compose.

### Prerrequisitos

Debes tener instalado [Docker Desktop](https://www.docker.com/products/docker-desktop/) (o Docker y Docker Compose en Linux).

### Instrucciones

1. Abre una terminal en la raíz del proyecto (donde se encuentra el archivo `docker-compose.yml`).
2. Ejecuta el siguiente comando para construir las imágenes y levantar los contenedores en segundo plano:

```bash
docker-compose up --build -d
```

*(Nota: Si usas versiones más recientes de Docker, el comando puede ser `docker compose` sin guion).*

3. **¡Listo!** Las aplicaciones estarán disponibles en:
   - Frontend: `http://localhost:3000`
   - Backend API: `http://localhost:8000`

Para detener los contenedores cuando termines, ejecuta:

```bash
docker-compose down
```
