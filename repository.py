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
        session.add(db_product)

    session.commit()


