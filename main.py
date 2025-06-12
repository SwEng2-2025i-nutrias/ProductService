import os
from flask import Flask
from app.config.db import db
from app.config.database import DatabaseConfig
from app.adapters.controller.product_controller import product_blueprint

def create_app():
    app = Flask(__name__)

    # Carga la configuración (BD, SECRET_KEY, etc.)
    app.config.from_object(DatabaseConfig)

    # Inicializar la base de datos
    db.init_app(app)
    print("SQLite DB path:", os.path.abspath("products.db"))
    # Registrar blueprints
    app.register_blueprint(product_blueprint, url_prefix="/api/v1/products")

    # Crear tablas si no existen (sólo en dev)
    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    debug_mode = DatabaseConfig.SECRET_KEY is None or False
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=debug_mode)
