from flask import Flask
from config.db import db
from app.adapters.controller.product_controller import product_blueprint

app = Flask(__name__)

# Configura tu conexión a PostgreSQL
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:root@localhost:5432/hex_crud"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(product_blueprint)

if __name__ == "__main__":
    app.run(debug=True)
