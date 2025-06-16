from flask import Flask
from app.config.db import db
from app.config.app_config import configure_app
from app.adapters.controller.product_controller import product_bp


def create_app():
    """Factory para crear la aplicación Flask"""
    app = Flask(__name__)
    
    # Configurar la aplicación
    configure_app(app)
    
    # Inicializar la base de datos
    db.init_app(app)
    
    # Registrar blueprints
    app.register_blueprint(product_bp)
    
    # Crear tablas si no existen (solo en desarrollo)
    with app.app_context():
        db.create_all()
    
    return app 