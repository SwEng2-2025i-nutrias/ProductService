class Product:
    def __init__(self, product_id: int, name: str, price: float):
        self.product_id = product_id
        self.name = name
        self.price = price

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "name": self.name,
            "price": self.price
        }
