from datetime import datetime
from typing import Optional

class Product:
    def __init__(self, product_id: int, name: str, price: float):
        self.product_id = product_id
        self.name       = name
        self.price      = price

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "name":       self.name,
            "price":      self.price
        }

    @property
    def total_value(self) -> float:
        """Calcula el valor total del producto (cantidad * precio por unidad)"""
        return self.quantity * self.price_per_unit

    def __str__(self):
        return f"Product(id={self.product_id}, name='{self.name}', type='{self.type}', quantity={self.quantity})"

    def __repr__(self):
        return self.__str__()