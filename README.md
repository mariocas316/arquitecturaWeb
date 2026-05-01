# Secret Share 🔒

Aplicación web diseñada para intercambiar mensajes encriptados de forma segura mediante un enlace. La característica principal de esta aplicación es que posee **cero persistencia**, lo que significa que los mensajes nunca se almacenan en ninguna base de datos ni memoria del servidor; el mensaje viaja encriptado y empaquetado de forma segura dentro del mismo enlace generado.

---

## 🛠️ Frameworks Seleccionados

1. **Backend**: [FastAPI](https://fastapi.tiangolo.com/)
   - Seleccionado por su altísimo rendimiento, su integración nativa con Pydantic para la validación estricta de datos y la autogeneración de documentación (Swagger UI).
2. **Frontend**: [Reflex](https://reflex.dev/)
   - Seleccionado por ser un framework *Full-Stack* basado 100% en Python, lo que permite desarrollar interfaces de usuario reactivas complejas sin necesidad de escribir Javascript, facilitando la unificación del lenguaje en todo el proyecto.

---

## 🏗️ Arquitectura de las Aplicaciones

### 1. Backend: Clean Architecture (Arquitectura Limpia)
El backend está estructurado bajo los principios de Clean Architecture para lograr un desacoplamiento total entre la lógica de negocio, las herramientas criptográficas y el framework web.

Sus capas (ubicadas en `backend/app/`) son:
- **`domain/` (Dominio):** Contiene las entidades principales y contratos de datos utilizando modelos de Pydantic (`MessageRequest`, `EncryptedMessageResponse`, etc.). No depende de nada externo.
- **`ports/` (Puertos):** Interfaces abstractas (Ej. `CryptoPort`) que definen cómo se debe comportar cualquier servicio criptográfico sin importar la librería subyacente.
- **`adapters/` (Adaptadores):** Implementaciones concretas de los puertos. Aquí vive `CryptoAdapter`, que utiliza la librería `cryptography` (AES-GCM y PBKDF2HMAC) para proveer encriptación de grado militar.
- **`use_cases/` (Casos de Uso):** Contienen la lógica pura del negocio (`EncryptMessageUseCase` y `DecryptMessageUseCase`). Orquestan los puertos pero ignoran completamente que están siendo ejecutados por FastAPI.
- **`api/` (Infraestructura / Entrypoint):** El marco de trabajo de FastAPI (`main.py`) que expone los endpoints, maneja CORS e inyecta las dependencias hacia los casos de uso.

### 2. Frontend: Arquitectura Modular de Reflex
El frontend está estructurado siguiendo las recomendaciones oficiales de escalabilidad de Reflex, separando responsabilidades estrictamente:

La estructura (ubicada en `frontend/frontend/`) es:
- **`state.py`:** Administra el estado global y las variables reactivas de la aplicación. Aquí residen todas las llamadas asíncronas HTTP (vía `httpx`) que se comunican con el Backend. Es el "cerebro" del frontend.
- **`styles.py`:** Centraliza los diccionarios de diseño, colores y variables de interfaz, permitiendo cambiar el "tema" de la aplicación tocando un solo archivo.
- **`pages/`:** Contiene la interfaz de usuario pura, desacoplada en diferentes vistas:
  - `index.py`: Página para escribir y encriptar un mensaje nuevo.
  - `read.py`: Página dedicada a recibir el payload de la URL y descifrar el mensaje.
- **`frontend.py`:** Actúa únicamente como enrutador principal para inicializar la aplicación de Reflex y registrar las páginas.

---

## 🚀 Cómo ejecutar el proyecto en tu entorno local

### Prerrequisitos del sistema
Debes tener instalado Python 3, `pip` y el paquete de entornos virtuales (`venv`). En sistemas basados en Debian/Ubuntu:
```bash
sudo apt update
sudo apt install python3-pip python3.12-venv
```

### Paso 1: Levantar el Backend (FastAPI)
Abre una terminal y colócate en la raíz del proyecto.
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn cryptography pydantic pydantic-settings
uvicorn app.api.main:app --reload
```
*El API quedará disponible en `http://localhost:8000`.*

### Paso 2: Levantar el Frontend (Reflex)
Abre una **nueva terminal** (sin cerrar la del backend) y colócate en la raíz del proyecto.
```bash
cd frontend
python3 -m venv venv
source venv/bin/activate
pip install reflex httpx
reflex init  # (Si pregunta por un template, presiona Enter para usar el Blank)
reflex run
```
*El Frontend quedará disponible en `http://localhost:3000`.*

### Paso 3: Probar
Abre tu navegador y entra a `http://localhost:3000`. ¡Escribe un mensaje, asigna una contraseña y genera tu enlace encriptado!

---
*Desarrollado para el proyecto de Arquitectura Web.*
