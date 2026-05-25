from PIL.ImageChops import offset
from charset_normalizer.api import explain_handler
from sqlalchemy import select
from sqlalchemy.orm import Session

from models import Product
from services.exchange_rate_service import get_exchange_rate, get_price_in_ron


def save_products_to_db(products_data, session):
    rates = {}
    for product in products_data:
        currency = product["currency"]

        if currency not in rates:
            rates[currency] = get_exchange_rate(currency)

        exchange_rate = rates[currency]

        if exchange_rate is None:
            continue

        price_ron = get_price_in_ron(product["price"], exchange_rate)

        existing_product = session.query(Product).filter_by(
            title=product["title"]
        ).first()

        if existing_product:
            existing_product.img = product["img"]
            existing_product.description = product["description"]
            existing_product.price = product["price"]
            existing_product.currency = currency
            existing_product.exchange_rate = exchange_rate
            existing_product.price_ron = price_ron
        else:
            db_product = Product(
                title=product["title"],
                img=product["img"],
                description =product["description"],
                price=product["price"],
                currency=currency,
                exchange_rate = exchange_rate,
                price_ron = price_ron
            )
            session.add(db_product) # equivalent for INSERT in SQL

    session.commit() # writes to the DB


def get_product_by_id(session, product_id):
    statement = select(Product).where(Product.id == product_id)

    return session.scalar(statement)


def get_all_products(session):
    return session.query(Product).all()


def update_product(session, product_id, new_product):
    product = get_product_by_id(session, product_id)

    if not product:
        return None

    currency = new_product["currency"]
    exchange_rate = get_exchange_rate(currency)

    if exchange_rate is None:
        return None

    price_ron = get_price_in_ron(new_product["price"], exchange_rate)

    product.title = new_product["title"]
    product.img = new_product["img"]
    product.description = new_product["description"]
    product.price = new_product["price"]
    product.currency = currency
    product.exchange_rate = exchange_rate
    product.price_ron = price_ron

    session.commit()
    session.refresh(product)

    return product


def delete_product(session, product_id):
    product = get_product_by_id(session, product_id)

    if not product:
        return False

    session.delete(product)
    session.commit()

    return True

def search_product_by_title(session: Session, keyword):
    return session.query(Product).filter(
        Product.title.ilike(f"%{keyword}%")
    ).all()