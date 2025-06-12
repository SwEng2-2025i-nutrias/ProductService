

from app.ports.product_repository_port import ProductRepositoryPort
from app.domain.product import Product

class ProductUseCase:
    def __init__(self, repository: ProductRepositoryPort):
        # Aquí el atributo se llama repository
        self.repository = repository

    def list_products(self):
        return self.repository.get_all()

    def get_product(self, product_id: int):
        return self.repository.get_by_id(product_id)

    def create_product(self, name: str, price: float) -> Product:
        # Asegúrate de que Product está importado arriba
        domain_prod = Product(product_id=None, name=name, price=price)
        # Usa self.repository, no self.repo
        return self.repository.create(domain_prod)

    def update_product(self, product_id: int, name: str, price: float):
        domain_prod = Product(product_id, name, price)
        return self.repository.update(product_id, domain_prod)

    def delete_product(self, product_id: int):
        return self.repository.delete(product_id)
