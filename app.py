import os.path
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from werkzeug.utils import secure_filename

from repository import get_all_products, get_product_by_id, update_product, delete_product, search_product_by_title
from database import SessionLocal
from services.csv_generator import generate_products_csv
from services.pdf_parser import extract_products_from_pdf

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
GENERATED_FOLDER= os.path.join(BASE_DIR, "generated")
ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.secret_key = "dev-secret-key"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def home():
    with SessionLocal() as session:
        products = get_all_products(session)

        return render_template("home.html", products=products)

@app.route("/products")
def get_all_products_page():
    search = request.args.get("search")

    with SessionLocal() as session:

        if search:
            products = search_product_by_title(session, search)
        else:
            products = get_all_products(session)

        return render_template("products.html", products=products, search=search)

@app.route("/products/<product_id>/edit", methods=["GET", "POST"])
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
                "price": request.form["price"],
                "currency": request.form["currency"]
            }
            update_product(session, product_id, new_product)

            return redirect(url_for("get_all_products_page"))

        return render_template("edit_product.html", product=product)


@app.route("/products/<product_id>/delete", methods=["POST"])
def delete_product_page(product_id):
    with SessionLocal() as session:
        product = get_product_by_id(session, product_id)

        if not product:
            return "No product found", 404

        if request.method == "POST":
            delete_product(session, product_id)

        return redirect(url_for("get_all_products_page"))

@app.route("/invoices/upload", methods=["GET", "POST"])
def upload_invoices():
    if request.method == "POST":
        if 'pdf' not in request.files:
            flash("No file part", "error")
            return redirect(request.url)

        file = request.files["pdf"]
        original_filename = file.filename

        if not original_filename:
            flash("No selected file", "error")
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

            flash("File uploaded", "success")
            return send_file(csv_path, as_attachment=True, download_name=f"{timestamp}_invoice.csv")

    return render_template("upload_invoice.html")