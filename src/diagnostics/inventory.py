class InventoryError(Exception):
    """Base exception for inventory errors."""


class InvalidQuantityError(InventoryError):
    """Raised when quantity is invalid."""


class ProductNotFoundError(InventoryError):
    """Raised when a product does not exist."""


class Product:
    def __init__(self, product_id, name, quantity):
        self.product_id = product_id
        self.name = name
        self._quantity = 0
        self.quantity = quantity

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        if not isinstance(value, int) or value < 0:
            raise InvalidQuantityError(
                "Quantity must be a non-negative integer."
            )
        self._quantity = value

    def get_details(self):
        return f"{self.product_id}: {self.name} - {self.quantity} units"


class PerishableProduct(Product):
    def __init__(self, product_id, name, quantity, expiry_date):
        super().__init__(product_id, name, quantity)
        self.expiry_date = expiry_date

    def get_details(self):
        return (
            f"{self.product_id}: {self.name} - "
            f"{self.quantity} units - Expires: {self.expiry_date}"
        )


class Inventory:
    def __init__(self):
        self._products = {}

    def add_product(self, product):
        self._products[product.product_id] = product

    def remove_product(self, product_id):
        if product_id not in self._products:
            raise ProductNotFoundError(
                f"Product '{product_id}' not found."
            )
        del self._products[product_id]

    def get_product(self, product_id):
        if product_id not in self._products:
            raise ProductNotFoundError(
                f"Product '{product_id}' not found."
            )
        return self._products[product_id]

    def list_products(self):
        return list(self._products.values())