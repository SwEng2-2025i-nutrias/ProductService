from app.ports.product_repository_port import ProductRepositoryPort
from app.domain.product import Product

class ProductUseCase:
    def __init__(self, repository: ProductRepositoryPort):
        self.repository = repository

    def list_products(self):
        return self.repository.get_all()

    def get_product(self, product_id: int):
        return self.repository.get_by_id(product_id)

    def create_product(self, product_id: int, name: str, price: float):
        product = Product(product_id, name, price)
        self.repository.create(product)

    def update_product(self, product_id: int, name: str, price: float):
        product = Product(product_id, name, price)
        return self.repository.update(product_id, product)

    def delete_product(self, product_id: int):
        return self.repository.delete(product_id)
