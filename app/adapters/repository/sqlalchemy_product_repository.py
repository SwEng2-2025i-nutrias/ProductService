from app.config.db import db
from app.domain.product import Product
from app.ports.product_repository_port import ProductRepositoryPort

class ProductModel(db.Model):
    __tablename__ = 'products'

    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def to_entity(self):
        return Product(self.product_id, self.name, self.price)

class SQLAlchemyProductRepository(ProductRepositoryPort):
    def get_all(self):
        return [p.to_entity() for p in ProductModel.query.all()]

    def get_by_id(self, product_id):
        model = ProductModel.query.get(product_id)
        return model.to_entity() if model else None

    def create(self, product):
        model = ProductModel(
            product_id=product.product_id,
            name=product.name,
            price=product.price
        )
        db.session.add(model)
        db.session.commit()

    def update(self, product_id, product):
        model = ProductModel.query.get(product_id)
        if model:
            model.name = product.name
            model.price = product.price
            db.session.commit()
            return True
        return False

    def delete(self, product_id):
        model = ProductModel.query.get(product_id)
        if model:
            db.session.delete(model)
            db.session.commit()
            return True
        return False
