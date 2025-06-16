import os
from flask_cors import CORS
from flasgger import Swagger


def configure_cors(app):
    """Configurar CORS para la aplicación"""
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:5173"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })


def configure_swagger(app):
    """Configurar Swagger/Flasgger para documentación API"""
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


def configure_database(app):
    """Configurar la base de datos"""
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        database_url = "sqlite:///productdb.db"
        print("⚠️  Usando SQLite para desarrollo local. Para producción configura DATABASE_URL en .env")
    
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


def configure_app(app):
    """Configurar todas las opciones de la aplicación"""
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "fallback-secret")
    
    configure_database(app)
    configure_cors(app)
    configure_swagger(app) 