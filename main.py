import os
from flask import Flask
from flasgger import Swagger
from app.config.db import db
from app.adapters.controller.product_controller import product_bp
from dotenv import load_dotenv
import os


# Carga las variables desde .env
load_dotenv()

def create_app():
    app = Flask(__name__)

    # Configuración desde variables de entorno
    database_url = os.getenv("DATABASE_URL")
    
    # Si no hay DATABASE_URL configurada, usar SQLite para desarrollo local
    if not database_url:
        database_url = "sqlite:///productdb.db"
        print("⚠️  Usando SQLite para desarrollo local. Para producción configura DATABASE_URL en .env")
    
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "fallback-secret")

    # Inicializar la base de datos
    db.init_app(app)

    # Configurar Flasgger (Swagger) simplificada
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec',
                "route": '/apispec.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/swagger/"
    }
    
    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "Product Service API",
            "description": "API REST para la gestión de productos - Arquitectura Hexagonal",
            "version": "1.0.0",
            "contact": {
                "name": "Product Service Team",
                "email": "team@productservice.com"
            }
        },
        "basePath": "/",
        "schemes": ["http", "https"],
        "consumes": ["application/json"],
        "produces": ["application/json"],
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "Token JWT en formato Bearer. Ejemplo: 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'"
            }
        },
        "tags": [
            {
                "name": "Products",
                "description": "Operaciones relacionadas con productos"
            }
        ]
    }
    
    Swagger(app, config=swagger_config, template=swagger_template)

    # Registrar blueprints
    app.register_blueprint(product_bp)

    # Crear tablas si no existen (sólo en dev)
    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    debug_mode = os.getenv("SECRET_KEY") is None or False
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=debug_mode)
