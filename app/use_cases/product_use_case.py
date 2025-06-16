from app.ports.product_repository_port import ProductRepositoryPort
from app.domain.product import Product
from datetime import datetime
from typing import Optional, Dict, Any

class ProductUseCase:
    def __init__(self, repository: ProductRepositoryPort):
        # Aquí el atributo se llama repository
        self.repository = repository

    def list_products(self):
        return self.repository.get_all()

    def get_product(self, product_id: int):
        return self.repository.get_by_id(product_id)
    
    def get_products_by_farm(self, farm_id: int):
        """
        Obtener todos los productos de una granja específica
        
        Args:
            farm_id: ID de la granja (obtenido del JWT)
            
        Returns:
            Lista de productos de la granja
        """
        return self.repository.get_by_farm_id(farm_id)

    def create_product(self, name: str, farm_id: int, type: str, 
                           quantity: int, price_per_unit: float, description: str, 
                           harvest_date: datetime):
        """Crear producto con todos los campos especificados"""
        product = Product(
            product_id=None,
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

    def patch_product(self, product_id: int, updates: Dict[str, Any]) -> Optional[Product]:
        """
        Actualizar parcialmente un producto con solo los campos proporcionados
        
        Args:
            product_id: ID del producto a actualizar
            updates: Diccionario con los campos a actualizar
            
        Returns:
            Product actualizado o None si no se encontró
        """
        # Verificar que el producto existe
        existing_product = self.repository.get_by_id(product_id)
        if not existing_product:
            return None
        
        # Validar que solo se actualicen campos permitidos
        allowed_fields = {
            'name', 'type', 'quantity', 'price_per_unit', 
            'description', 'harvest_date'
        }
        
        invalid_fields = set(updates.keys()) - allowed_fields
        if invalid_fields:
            raise ValueError(f"Campos no permitidos para actualización: {', '.join(invalid_fields)}")
        
        # Validar tipos de datos
        if 'quantity' in updates and not isinstance(updates['quantity'], int):
            raise ValueError("quantity debe ser un número entero")
        
        if 'price_per_unit' in updates and not isinstance(updates['price_per_unit'], (int, float)):
            raise ValueError("price_per_unit debe ser un número")
        
        if 'harvest_date' in updates and isinstance(updates['harvest_date'], str):
            try:
                updates['harvest_date'] = datetime.fromisoformat(updates['harvest_date'].replace('Z', '+00:00'))
            except ValueError:
                raise ValueError("harvest_date debe tener formato ISO (YYYY-MM-DDTHH:MM:SS)")
        
        # Llamar al repositorio para actualización parcial
        success = self.repository.patch(product_id, updates)
        
        if success:
            # Retornar el producto actualizado
            return self.repository.get_by_id(product_id)
        
        return None

    def delete_product(self, product_id: int):
        return self.repository.delete(product_id)
