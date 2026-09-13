import csv
import json

from diagnostics.inventory import Product, PerishableProduct


def save_json(inventory, file_path):
    data = []

    for product in inventory.list_products():
        item = {
            "product_id": product.product_id,
            "name": product.name,
            "quantity": product.quantity,
        }

        if isinstance(product, PerishableProduct):
            item["expiry_date"] = product.expiry_date

        data.append(item)

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)


def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    products = []

    for item in data:
        if "expiry_date" in item:
            product = PerishableProduct(
                item["product_id"],
                item["name"],
                item["quantity"],
                item["expiry_date"],
            )
        else:
            product = Product(
                item["product_id"],
                item["name"],
                item["quantity"],
            )

        products.append(product)

    return products


def save_csv(inventory, file_path):
    with open(file_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["product_id", "name", "quantity", "expiry_date"],
        )

        writer.writeheader()

        for product in inventory.list_products():
            writer.writerow({
                "product_id": product.product_id,
                "name": product.name,
                "quantity": product.quantity,
                "expiry_date": getattr(product, "expiry_date", ""),
            })


def load_csv(file_path):
    products = []

    with open(file_path, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            quantity = int(row["quantity"])

            if row["expiry_date"]:
                product = PerishableProduct(
                    row["product_id"],
                    row["name"],
                    quantity,
                    row["expiry_date"],
                )
            else:
                product = Product(
                    row["product_id"],
                    row["name"],
                    quantity,
                )

            products.append(product)

    return products