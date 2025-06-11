from flask import Blueprint, jsonify, request
from app.use_cases.product_use_case import ProductUseCase
from app.adapters.repository.sqlalchemy_product_repository import SQLAlchemyProductRepository

product_blueprint = Blueprint("product", __name__)
repository = SQLAlchemyProductRepository()
use_case = ProductUseCase(repository)

@product_blueprint.route("", methods=["GET"])
def get_all_products():
    products = use_case.list_products()
    return jsonify([p.to_dict() for p in products])

@product_blueprint.route("/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = use_case.get_product(product_id)
    if product:
        return jsonify(product.to_dict())
    return jsonify({"error": "Product not found"}), 404

@product_blueprint.route("", methods=["POST"])
def create_product():
    data = request.get_json()
    use_case.create_product(data["product_id"], data["name"], data["price"])
    return jsonify({"message": "Product created"}), 201

@product_blueprint.route("/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    data = request.get_json()
    updated = use_case.update_product(product_id, data["name"], data["price"])
    if updated:
        return jsonify({"message": "Product updated"})
    return jsonify({"error": "Product not found"}), 404

@product_blueprint.route("/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    deleted = use_case.delete_product(product_id)
    if deleted:
        return jsonify({"message": "Product deleted"})
    return jsonify({"error": "Product not found"}), 404
