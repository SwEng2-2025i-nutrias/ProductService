

from app.ports.product_repository_port import ProductRepositoryPort
from app.domain.product import Product
from datetime import datetime

class ProductUseCase:
    def __init__(self, repository: ProductRepositoryPort):
        # Aquí el atributo se llama repository
        self.repository = repository

    def list_products(self):
        return self.repository.get_all()

    def get_product(self, product_id: int):
        return self.repository.get_by_id(product_id)
    

    def create_product(self, product_id: int, name: str, farm_id: int, type: str, 
                           quantity: int, price_per_unit: float, description: str, 
                           harvest_date: datetime):
        """Crear producto con todos los campos especificados"""
        product = Product(
            product_id=product_id,
            name=name,
            farm_id=farm_id,
            type=type,
            quantity=quantity,
            price_per_unit=price_per_unit,
            description=description,
            harvest_date=harvest_date
        )
        self.repository.create(product)

    def update_product(self, product_id: int, name: str, price: float):
        # Actualizar producto con valores por defecto para demo/desarrollo
        product = Product(
            product_id=product_id,
            name=name,
            farm_id=1,  # Valor por defecto
            type="General",  # Valor por defecto
            quantity=10,  # Valor por defecto
            price_per_unit=price,
            description=f"Producto actualizado {name}",  # Descripción por defecto
            harvest_date=datetime.now()  # Fecha actual
        )
        return self.repository.update(product_id, product)

    def update_product_full(self, product_id: int, name: str, farm_id: int, type: str,
                           quantity: int, price_per_unit: float, description: str,
                           harvest_date: datetime):
        """Actualizar producto con todos los campos especificados"""
        product = Product(
            product_id=product_id,
            name=name,
            farm_id=farm_id,
            type=type,
            quantity=quantity,
            price_per_unit=price_per_unit,
            description=description,
            harvest_date=harvest_date
        )
        return self.repository.update(product_id, product)

    def delete_product(self, product_id: int):
        return self.repository.delete(product_id)
