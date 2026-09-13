import unittest

from diagnostics.inventory import (
    Inventory,
    InvalidQuantityError,
    PerishableProduct,
    Product,
    ProductNotFoundError,
)

from diagnostics.storage import (
    load_csv,
    load_json,
    save_csv,
    save_json,
)


class TestInventory(unittest.TestCase):

    def setUp(self):
        self.inventory = Inventory()

        self.product = Product("P001", "Keyboard", 10)

        self.perishable = PerishableProduct(
            "P002",
            "Milk",
            5,
            "2026-12-31",
        )

    def test_add_and_get_product(self):
        self.inventory.add_product(self.product)

        result = self.inventory.get_product("P001")

        self.assertEqual(result.name, "Keyboard")
        self.assertEqual(result.quantity, 10)

    def test_invalid_quantity(self):
        with self.assertRaises(InvalidQuantityError):
            Product("P003", "Mouse", -5)

    def test_product_not_found(self):
        with self.assertRaises(ProductNotFoundError):
            self.inventory.get_product("UNKNOWN")

    def test_inheritance_and_polymorphism(self):
        self.inventory.add_product(self.perishable)

        result = self.perishable.get_details()

        self.assertIn("Expires: 2026-12-31", result)
        self.assertIsInstance(self.perishable, Product)

    def test_json_persistence(self):
        self.inventory.add_product(self.product)
        self.inventory.add_product(self.perishable)

        file_path = "test_inventory.json"

        save_json(self.inventory, file_path)

        products = load_json(file_path)

        self.assertEqual(len(products), 2)
        self.assertEqual(products[0].name, "Keyboard")
        self.assertEqual(products[1].expiry_date, "2026-12-31")

    def test_csv_persistence(self):
        self.inventory.add_product(self.product)

        file_path = "test_inventory.csv"

        save_csv(self.inventory, file_path)

        products = load_csv(file_path)

        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].name, "Keyboard")
        self.assertEqual(products[0].quantity, 10)


if __name__ == "__main__":
    unittest.main()