from flask import Blueprint, jsonify, request
from app.use_cases.product_use_case import ProductUseCase
from app.adapters.repository.sqlalchemy_product_repository import SQLAlchemyProductRepository

# Definimos el blueprint con url_prefix '/products'
product_blueprint = Blueprint("products", __name__, url_prefix="/products")

# Inyectamos el repositorio y el caso de uso
repository = SQLAlchemyProductRepository()
use_case = ProductUseCase(repository)

@product_blueprint.route("/", methods=["GET"])
def get_all_products():
    products = use_case.list_products()
    return jsonify([p.to_dict() for p in products]), 200

@product_blueprint.route("/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = use_case.get_product(product_id)
    if product:
        return jsonify(product.to_dict()), 200
    return jsonify({"error": "Product not found"}), 404

@product_blueprint.route("/", methods=["POST"])
def create_product():
    data = request.get_json() or {}

    # Validación mínima
    if "name" not in data or "price" not in data:
        return jsonify({"error": "Faltan campos 'name' o 'price'"}), 400

    # Llamamos al caso de uso
    created = use_case.create_product(
        name=data["name"],
        price=data["price"]
    )

    return jsonify(created.to_dict()), 201

@product_blueprint.route("/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    data = request.get_json() or {}
    if "name" not in data or "price" not in data:
        return jsonify({"error": "Faltan campos 'name' o 'price'"}), 400

    updated = use_case.update_product(
        product_id,
        name=data["name"],
        price=data["price"]
    )
    if updated:
        return jsonify({"message": "Product updated"}), 200
    return jsonify({"error": "Product not found"}), 404

@product_blueprint.route("/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    deleted = use_case.delete_product(product_id)
    if deleted:
        return jsonify({"message": "Product deleted"}), 200
    return jsonify({"error": "Product not found"}), 404

