from abc import ABC, abstractmethod
from app.domain.product import Product
from typing import List, Optional, Dict, Any

class ProductRepositoryPort(ABC):
    @abstractmethod
    def get_all(self) -> List[Product]:
        pass

    @abstractmethod
    def get_by_id(self, product_id: int) -> Optional[Product]:
        pass

    @abstractmethod
    def create(self, product: Product) -> None:
        pass

    @abstractmethod
    def update(self, product_id: int, product: Product) -> bool:
        pass

    @abstractmethod
    def patch(self, product_id: int, updates: Dict[str, Any]) -> bool:
        """
        Actualizar parcialmente un producto con solo los campos proporcionados
        
        Args:
            product_id: ID del producto a actualizar
            updates: Diccionario con los campos a actualizar
            
        Returns:
            True si se actualizó correctamente, False si no se encontró el producto
        """
        pass

    @abstractmethod
    def delete(self, product_id: int) -> bool:
        pass
