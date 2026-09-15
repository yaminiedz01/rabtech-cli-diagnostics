import argparse
import json
import time
from datetime import datetime

import requests
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def login(base_url, username, password):
    response = requests.post(
        f"{base_url}/login",
        data={
            "username": username,
            "password": password,
        },
        timeout=10,
    )
    response.raise_for_status()
    return response.json()["access_token"]


def fetch_products(base_url, token):
    response = requests.get(
        f"{base_url}/products",
        headers={"Authorization": f"Bearer {token}"},
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


def generate_statistics(products):
    total_products = len(products)
    total_quantity = sum(product["quantity"] for product in products)

    average_quantity = (
        total_quantity / total_products
        if total_products
        else 0
    )

    return {
        "total_products": total_products,
        "total_quantity": total_quantity,
        "average_quantity": round(average_quantity, 2),
    }


def create_pdf(products, statistics, output_file):
    pdf = canvas.Canvas(output_file, pagesize=A4)

    width, height = A4
    y = height - 50

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(50, y, "RabTech Inventory Automation Report")

    y -= 30
    pdf.setFont("Helvetica", 10)
    pdf.drawString(
        50,
        y,
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
    )

    y -= 40

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y, "Summary")

    y -= 25
    pdf.setFont("Helvetica", 11)

    pdf.drawString(
        60,
        y,
        f"Total Products: {statistics['total_products']}",
    )

    y -= 20
    pdf.drawString(
        60,
        y,
        f"Total Quantity: {statistics['total_quantity']}",
    )

    y -= 20
    pdf.drawString(
        60,
        y,
        f"Average Quantity: {statistics['average_quantity']}",
    )

    y -= 40

    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(50, y, "Product Details")

    y -= 25

    pdf.setFont("Helvetica", 10)

    for product in products:
        line = (
            f"ID: {product['id']} | "
            f"Name: {product['name']} | "
            f"Quantity: {product['quantity']}"
        )

        pdf.drawString(60, y, line)
        y -= 20

        if y < 50:
            pdf.showPage()
            y = height - 50
            pdf.setFont("Helvetica", 10)

    pdf.save()


def save_json_report(statistics, output_file):
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(statistics, file, indent=2)


def run_report(base_url, username, password, pdf_file, json_file):
    print("Logging in to Inventory API...")

    token = login(base_url, username, password)

    print("Authentication successful.")

    products = fetch_products(base_url, token)

    print(f"Fetched {len(products)} products.")

    statistics = generate_statistics(products)

    create_pdf(products, statistics, pdf_file)
    save_json_report(statistics, json_file)

    print("=== Automation Report ===")
    print(f"Total Products  : {statistics['total_products']}")
    print(f"Total Quantity   : {statistics['total_quantity']}")
    print(f"Average Quantity : {statistics['average_quantity']}")
    print(f"PDF saved to     : {pdf_file}")
    print(f"JSON saved to    : {json_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Automated Inventory Report Generator"
    )

    parser.add_argument(
        "--url",
        default="http://127.0.0.1:8000",
        help="Inventory API base URL",
    )

    parser.add_argument(
        "--username",
        required=True,
        help="API username",
    )

    parser.add_argument(
        "--password",
        required=True,
        help="API password",
    )

    parser.add_argument(
        "--pdf",
        default="inventory_report.pdf",
        help="PDF output file",
    )

    parser.add_argument(
        "--json",
        default="inventory_report.json",
        help="JSON output file",
    )

    parser.add_argument(
        "--schedule",
        type=int,
        default=0,
        help="Repeat report every N seconds",
    )

    args = parser.parse_args()

    if args.schedule > 0:
        while True:
            run_report(
                args.url,
                args.username,
                args.password,
                args.pdf,
                args.json,
            )

            print(
                f"Waiting {args.schedule} seconds "
                "before the next report..."
            )

            time.sleep(args.schedule)
    else:
        run_report(
            args.url,
            args.username,
            args.password,
            args.pdf,
            args.json,
        )


if __name__ == "__main__":
    main()