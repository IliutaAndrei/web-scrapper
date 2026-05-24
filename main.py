from database import SessionLocal
from scraper import scrape_products
from repository import save_products_to_db


def run_scraper():
    products_data = scrape_products()

    with SessionLocal() as session:
        save_products_to_db(products_data, session)

    print(f"Processed {len(products_data)} products")


if __name__ == "__main__":
    run_scraper()
