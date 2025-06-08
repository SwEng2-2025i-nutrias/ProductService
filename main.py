from flask import Flask
from app.config.db import db
from app.adapters.controller.product_controller import product_blueprint
from dotenv import load_dotenv
import os


# Carga las variables desde .env
load_dotenv()

def create_app():
    app = Flask(__name__)

    # Configuración desde variables de entorno
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "fallback-secret")

    # Inicializar la base de datos
    db.init_app(app)

    # Registrar blueprints
    app.register_blueprint(product_blueprint)

    # Crear tablas si no existen (solo útil en desarrollo)
    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    # Obtener valores del entorno
    debug_mode = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    env = os.getenv("FLASK_ENV", "production")

    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=debug_mode)