from sqlalchemy import select
from sqlalchemy.orm import Session

from models import Product


def save_products_to_db(products_data, session):
    for product in products_data:

        existing_product = session.query(Product).filter_by(
            title=product["title"]
        ).first()

        if existing_product:
            existing_product.img = product["img"]
            existing_product.description = product["description"]
            existing_product.price = product["price"]
            existing_product.currency = product["currency"]
        else:
            db_product = Product(
                title=product["title"],
                img=product["img"],
                description =product["description"],
                price=product["price"],
                currency=product["currency"]
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

    product.title = new_product["title"]
    product.img = new_product["img"]
    product.description = new_product["description"]
    product.price = new_product["price"]
    product.currency = new_product["currency"]

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