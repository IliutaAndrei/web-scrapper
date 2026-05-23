from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy.engine import url

from repository import get_all_products, get_product_by_id, update_product
from database import SessionLocal
app = Flask(__name__)

@app.route("/products")
def get_all_products_page():
    with SessionLocal() as session:
        products = get_all_products(session)

    return render_template("products.html", products=products)

@app.route("/products/<int:product_id>/edit", methods=["GET", "POST"])
def edit_product_page(product_id):
    with SessionLocal() as session:
        product = get_product_by_id(session, product_id)
        if not product:
            return "No product Found", 404

        if request.method == "POST":
            new_product = {
                "title": request.form["title"],
                "img": request.form["img"],
                "description": request.form["description"],
                "price": request.form["price"]
            }
            update_product(session, product_id, new_product)

            return redirect(url_for("get_all_products_page"))

    return render_template("edit_product_page.html", product=product)