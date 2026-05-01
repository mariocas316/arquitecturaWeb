from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

"""
Módulo de configuración de la Base de Datos.
Establece la conexión usando SQLAlchemy hacia una base de datos SQLite local
como medio de persistencia efímera manejada por el ORM.
"""

SQLALCHEMY_DATABASE_URL = "sqlite:///./sqlite.db"

# Creación del motor de base de datos. check_same_thread=False es requerido para SQLite en FastAPI.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Fábrica de sesiones para interactuar con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base declarativa de la cual heredarán los modelos del ORM
Base = declarative_base()

def get_db():
    """
    Dependencia de FastAPI para inyectar la sesión de la base de datos en las rutas.
    Abre una conexión al inicio de la petición y la cierra al finalizar.
    
    Yields:
        Session: Sesión activa de SQLAlchemy.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
