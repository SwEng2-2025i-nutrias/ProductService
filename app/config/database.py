import os
from dotenv import load_dotenv

# Carga variables de entorno de .env
load_dotenv()

class DatabaseConfig:
    # URI de la BD: primero mira DATABASE_URL, si no existe, usa SQLite
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        # Tres slashes = fichero relativo; cuatro slashes = absoluto
        "sqlite:///./products.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret")
