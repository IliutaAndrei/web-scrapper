import os.path
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, send_file, session as login_session
from sqlalchemy.orm import Session
from werkzeug.utils import secure_filename

from repository import get_all_products, get_product_by_id, update_product, delete_product, search_product_by_title
from database import engine
from services.csv_generator import generate_products_csv
from services.pdf_parser import extract_products_from_pdf

from config import SESSION_SECRET_KEY, UPLOAD_FOLDER, allowed_file, GENERATED_FOLDER, ADMIN_PASSWORD, ADMIN_USERNAME

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["SECRET_KEY"] = SESSION_SECRET_KEY

@app.after_request
def add_no_cache_headers(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"

    return response


@app.before_request
def require_login():
    allowed_routes = ["login", "static"]

    if request.endpoint in allowed_routes:
        return None

    if login_session.get("is_logged_in"):
        return None

    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            login_session["is_logged_in"] = True

            return redirect(url_for("home"))

        return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")


@app.route("/logout")
def logout():
    login_session.pop("is_logged_in", None)

    return redirect(url_for("login"))


@app.route("/")
def home():
    with Session(engine) as db_session:
        products = get_all_products(db_session)

        return render_template("home.html", products=products)


@app.route("/products")
def get_all_products_page():
    search = request.args.get("search")

    with Session(engine) as db_session:

        if search:
            products = search_product_by_title(db_session, search)
        else:
            products = get_all_products(db_session)

        return render_template("products.html", products=products, search=search)


@app.route("/products/<int:product_id>/edit", methods=["GET", "POST"])
def edit_product_page(product_id):
    with Session(engine) as db_session:
        product = get_product_by_id(db_session, product_id)

        if not product:
            return "No product Found", 404

        if request.method == "POST":
            new_product = {
                "title": request.form["title"],
                "img": request.form["img"],
                "description": request.form["description"],
                "price": request.form["price"],
                "currency": request.form["currency"]
            }
            try:
                updated_product = update_product(db_session, product_id, new_product)
            except ValueError as error:
                return render_template("edit_product.html", product=product, error=error)

            if not updated_product:
                return render_template("edit_product.html",
                                       product=product,
                                       error="Check the currency")

            return redirect(url_for("get_all_products_page"))

        return render_template("edit_product.html", product=product)


@app.route("/products/<int:product_id>/delete", methods=["POST"])
def delete_product_page(product_id):
    with Session(engine) as db_session:
        product = get_product_by_id(db_session, product_id)

        if not product:
            return "No product found", 404


        delete_product(db_session, product_id)

        return redirect(url_for("get_all_products_page"))


@app.route("/invoices/upload", methods=["GET", "POST"])
def upload_invoices():
    if request.method == "POST":
        if 'pdf' not in request.files:
            return redirect(request.url)

        file = request.files["pdf"]
        original_filename = file.filename

        if not original_filename:
            return redirect(request.url)

        if file and allowed_file(original_filename):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = secure_filename(original_filename)
            unique_filename = f"{timestamp}_{filename}"

            file_path = os.path.join(app.config["UPLOAD_FOLDER"], unique_filename)
            file.save(file_path)

            csv_filename = f"{timestamp}_invoices_products.csv"
            csv_path = os.path.join(GENERATED_FOLDER, csv_filename)

            products = extract_products_from_pdf(file_path)
            generate_products_csv(products,csv_path)

            return send_file(csv_path, as_attachment=True, download_name=f"{timestamp}_invoice.csv")

    return render_template("upload_invoice.html")