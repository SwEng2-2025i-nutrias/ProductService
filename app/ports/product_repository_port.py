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
    def get_by_farm_id(self, farm_id: int) -> List[Product]:
     
        pass

    @abstractmethod
    def create(self, product: Product) -> None:
        pass

    @abstractmethod
    def update(self, product_id: int, product: Product) -> bool:
        pass

    @abstractmethod
    def patch(self, product_id: int, updates: Dict[str, Any]) -> bool:
        pass

    @abstractmethod
    def delete(self, product_id: int) -> bool:
        pass
