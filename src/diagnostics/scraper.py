import csv
import json
import time

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


URL = "https://books.toscrape.com/"
OUTPUT_FILE = "output.csv"
REPORT_FILE = "report.json"


def create_session():
    session = requests.Session()

    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
    )

    adapter = HTTPAdapter(max_retries=retry_strategy)

    session.mount("https://", adapter)
    session.mount("http://", adapter)

    session.headers.update({
        "User-Agent": "RabTech-Internship-Scraper/1.0"
    })

    return session


def scrape_books():
    session = create_session()

    response = session.get(URL, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    books = []

    for book in soup.select("article.product_pod"):
        title = book.h3.a.get("title", "").strip()

        price = book.select_one(".price_color").get_text(
            strip=True
        )

        availability = book.select_one(
            ".availability"
        ).get_text(" ", strip=True)

        books.append({
            "title": title,
            "price": price,
            "availability": availability,
        })

        # Rate limiting
        time.sleep(0.2)

    return books


def save_csv(books):
    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "title",
                "price",
                "availability"
            ],
        )

        writer.writeheader()
        writer.writerows(books)


def generate_report(books):
    total_books = len(books)

    available_books = sum(
        1
        for book in books
        if "In stock" in book["availability"]
    )

    availability_rate = (
        (available_books / total_books) * 100
        if total_books
        else 0
    )

    return {
        "total_books": total_books,
        "available_books": available_books,
        "availability_rate_percent": round(
            availability_rate,
            2
        ),
    }


def save_report(report):
    with open(
        REPORT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            report,
            file,
            indent=2
        )


if __name__ == "__main__":

    books = scrape_books()

    save_csv(books)

    report = generate_report(books)

    save_report(report)

    print("=== Web Scraping Report ===")
    print(
        f"Total books       : "
        f"{report['total_books']}"
    )
    print(
        f"Available books   : "
        f"{report['available_books']}"
    )
    print(
        f"Availability rate : "
        f"{report['availability_rate_percent']}%"
    )
    print(
        f"CSV saved to      : "
        f"{OUTPUT_FILE}"
    )
    print(
        f"Report saved to   : "
        f"{REPORT_FILE}"
    )