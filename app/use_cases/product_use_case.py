from app.ports.product_repository_port import ProductRepositoryPort
from app.domain.product import Product
from datetime import datetime
from typing import Optional, Dict, Any

class ProductUseCase:
    def __init__(self, repository: ProductRepositoryPort):
       
        self.repository = repository

    def list_products(self):
        return self.repository.get_all()

    def get_product(self, product_id: int):
        return self.repository.get_by_id(product_id)
    
    def get_products_by_farm(self, farm_id: str):
       
        return self.repository.get_by_farm_id(farm_id)

    def create_product(self, name: str, farm_id: str, type: str, 
                           quantity: int, price_per_unit: float, description: str, 
                           harvest_date: datetime):
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
        product = Product(
            product_id=product_id,
            name=name,
            farm_id="1",  
            type="General",  
            quantity=10,  
            price_per_unit=price,
            description=f"Producto actualizado {name}",  
            harvest_date=datetime.now()  
        )
        return self.repository.update(product_id, product)

    def update_product_full(self, product_id: int, name: str, farm_id: str, type: str,
                           quantity: int, price_per_unit: float, description: str,
                           harvest_date: datetime):
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
  
        existing_product = self.repository.get_by_id(product_id)
        if not existing_product:
            return None
        
       
        allowed_fields = {
            'name', 'type', 'quantity', 'price_per_unit', 
            'description', 'harvest_date'
        }
        
        invalid_fields = set(updates.keys()) - allowed_fields
        if invalid_fields:
            raise ValueError(f"Campos no permitidos para actualización: {', '.join(invalid_fields)}")
        
       
        if 'quantity' in updates and not isinstance(updates['quantity'], int):
            raise ValueError("quantity debe ser un número entero")
        
        if 'price_per_unit' in updates and not isinstance(updates['price_per_unit'], (int, float)):
            raise ValueError("price_per_unit debe ser un número")
        
        if 'harvest_date' in updates and isinstance(updates['harvest_date'], str):
            try:
                updates['harvest_date'] = datetime.fromisoformat(updates['harvest_date'].replace('Z', '+00:00'))
            except ValueError:
                raise ValueError("harvest_date debe tener formato ISO (YYYY-MM-DDTHH:MM:SS)")
        
       
        success = self.repository.patch(product_id, updates)
        
        if success:
           
            return self.repository.get_by_id(product_id)
        
        return None

    def delete_product(self, product_id: int):
        return self.repository.delete(product_id)
