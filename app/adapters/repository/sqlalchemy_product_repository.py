from app.config.db import db
from app.domain.product import Product
from app.ports.product_repository_port import ProductRepositoryPort
from datetime import datetime
from typing import Dict, Any

class ProductModel(db.Model):
    __tablename__ = 'products'

    product_id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(100), nullable=False)
    farm_id: int = db.Column(db.Integer, nullable=False)
    type: str = db.Column(db.String(100), nullable=False)
    quantity: int = db.Column(db.Integer, nullable=False)
    price_per_unit: float = db.Column(db.Float, nullable=False)
    description: str = db.Column(db.String(255), nullable=False)
    harvest_date: datetime = db.Column(db.DateTime, nullable=False)
    created_at: datetime = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_entity(self):
        return Product(
            product_id=self.product_id,
            name=self.name,
            farm_id=self.farm_id,
            type=self.type,
            quantity=self.quantity,
            price_per_unit=self.price_per_unit,
            description=self.description,
            harvest_date=self.harvest_date,
            created_at=self.created_at
        )

class SQLAlchemyProductRepository(ProductRepositoryPort):
    def get_all(self):
        return [p.to_entity() for p in ProductModel.query.all()]

    def get_by_id(self, product_id):
        model = ProductModel.query.get(product_id)
        return model.to_entity() if model else None

    def get_by_farm_id(self, farm_id: int):
       
        models = ProductModel.query.filter_by(farm_id=farm_id).all()
        return [model.to_entity() for model in models]

    def create(self, product):
        model = ProductModel(
            name=product.name,
            farm_id=product.farm_id,
            type=product.type,
            quantity=product.quantity,
            price_per_unit=product.price_per_unit,
            description=product.description,
            harvest_date=product.harvest_date
        )
        db.session.add(model)
        db.session.commit()
        product.product_id = model.product_id
        return product

    def update(self, product_id, product):
        model = ProductModel.query.get(product_id)
        if model:
            model.name = product.name
            model.farm_id = product.farm_id
            model.type = product.type
            model.quantity = product.quantity
            model.price_per_unit = product.price_per_unit
            model.description = product.description
            model.harvest_date = product.harvest_date
            db.session.commit()
            return True
        return False

    def patch(self, product_id: int, updates: Dict[str, Any]) -> bool:
        model = ProductModel.query.get(product_id)
        if not model:
            return False
        
        field_mapping = {
            'name': 'name',
            'type': 'type',
            'quantity': 'quantity',
            'price_per_unit': 'price_per_unit',
            'description': 'description',
            'harvest_date': 'harvest_date'
        }
        
        for field, value in updates.items():
            if field in field_mapping:
                setattr(model, field_mapping[field], value)
        
        try:
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False

    def delete(self, product_id):
        model = ProductModel.query.get(product_id)
        if model:
            db.session.delete(model)
            db.session.commit()
            return True
        return False
