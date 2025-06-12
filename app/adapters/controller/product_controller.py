from flask import request, Blueprint, jsonify
from flasgger import swag_from
from app.use_cases.product_use_case import ProductUseCase
from app.adapters.repository.sqlalchemy_product_repository import SQLAlchemyProductRepository
from datetime import datetime
import os

# Crear blueprint para productos
product_bp = Blueprint('products', __name__, url_prefix='/api/v1/products')

# Inicializar repositorio y caso de uso
repository = SQLAlchemyProductRepository()
use_case = ProductUseCase(repository)

# Obtener la ruta base del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
SWAGGER_DIR = os.path.join(BASE_DIR, 'app', 'docs', 'swagger')

@product_bp.route('', methods=['GET'])
@swag_from(os.path.join(SWAGGER_DIR, 'get_all_products.yml'))
def get_all_products(): 
    """Obtener todos los productos"""
    try:
        products = use_case.list_products()
        return jsonify([p.to_dict() for p in products]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@product_bp.route('', methods=['POST'])
@swag_from(os.path.join(SWAGGER_DIR, 'create_product.yml'))
def create_product():
    """Crear un nuevo producto"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Validar campos requeridos básicos
        required_fields = ['product_id', 'name', 'farm_id', 'type', 'quantity', 'price_per_unit', 'description']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400
        
        # Parsear fecha de cosecha si se proporciona
        harvest_date = datetime.now()
        if 'harvest_date' in data and data['harvest_date']:
            try:
                harvest_date = datetime.fromisoformat(data['harvest_date'].replace('Z', '+00:00'))
            except ValueError:
                return jsonify({"error": "Invalid harvest_date format. Use ISO format"}), 400
        
        use_case.create_product_full(
            product_id=data["product_id"],
            name=data["name"],
            farm_id=data["farm_id"],
            type=data["type"],
            quantity=data["quantity"],
            price_per_unit=data["price_per_unit"],
            description=data["description"],
            harvest_date=harvest_date
        )
        return jsonify({"message": "Product created"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@product_bp.route('/<int:product_id>', methods=['GET'])
@swag_from(os.path.join(SWAGGER_DIR, 'get_product_by_id.yml'))
def get_product(product_id):
    """Obtener un producto por su ID"""
    try:
        product = use_case.get_product(product_id)
        if product:
            return jsonify(product.to_dict()), 200
        return jsonify({"error": "Product not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@product_bp.route('/<int:product_id>', methods=['PUT'])
@swag_from(os.path.join(SWAGGER_DIR, 'update_product.yml'))
def update_product(product_id):
    """Actualizar un producto existente"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Obtener el producto existente
        existing_product = use_case.get_product(product_id)
        if not existing_product:
            return jsonify({"error": "Product not found"}), 404
        
        # Parsear fecha de cosecha si se proporciona
        harvest_date = existing_product.harvest_date
        if 'harvest_date' in data and data['harvest_date']:
            try:
                harvest_date = datetime.fromisoformat(data['harvest_date'].replace('Z', '+00:00'))
            except ValueError:
                return jsonify({"error": "Invalid harvest_date format. Use ISO format"}), 400
        
        updated = use_case.update_product_full(
            product_id=product_id,
            name=data.get("name", existing_product.name),
            farm_id=data.get("farm_id", existing_product.farm_id),
            type=data.get("type", existing_product.type),
            quantity=data.get("quantity", existing_product.quantity),
            price_per_unit=data.get("price_per_unit", existing_product.price_per_unit),
            description=data.get("description", existing_product.description),
            harvest_date=harvest_date
        )
        if updated:
            return jsonify({"message": "Product updated"}), 200
        return jsonify({"error": "Failed to update product"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@product_bp.route('/<int:product_id>', methods=['DELETE'])
@swag_from(os.path.join(SWAGGER_DIR, 'delete_product.yml'))
def delete_product(product_id):
    """Eliminar un producto"""
    try:
        deleted = use_case.delete_product(product_id)
        if deleted:
            return jsonify({"message": "Product deleted"}), 200
        return jsonify({"error": "Product not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
