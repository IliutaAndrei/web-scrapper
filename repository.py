from sqlalchemy import select, Boolean
from models import Product


def save_products_to_db(products_data, session):
    for product in products_data:

        existing_product = session.query(Product).filter_by(
            title=product["title"]
        ).first()

        if existing_product:
            continue

        db_product = Product(
            title=product["title"],
            img=product["img"],
            description =product["description"],
            price=product["price"]
        )
        session.add(db_product) # equivalent for INSERT in SQL

    session.commit() # writes to the DB


def get_product_by_id(session, product_id):
    statement = select(Product).where(Product.id == product_id)

    return session.scalar(statement)


def get_all_products(session):
    statement = select(Product)

    return session.scalars(statement).all()


def update_product(session, product_id, new_product):
    product = get_product_by_id(session, product_id)

    if not product:
        return None

    product.title = new_product["title"]
    product.img = new_product["img"]
    product.description = new_product["description"]
    product.price = new_product["price"]

    session.commit()

    return product


def delete_product(session, product_id):
    product = get_product_by_id(session, product_id)

    if not product:
        return False

    session.delete(product)
    session.commit()

    return True