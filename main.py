from database import SessionLocal
from scraper import scrape_products
from repository import save_products_to_db

with SessionLocal() as session:
    products_data = scrape_products()
    save_products_to_db(products_data, session)
