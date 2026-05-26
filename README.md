# Web Products Scraper & Invoice Parser

A Python web application that logs into a target website, scrapes product data, stores it in a SQL database, and provides a simple Flask interface for viewing, searching, editing, and deleting products.

The project also includes a PDF invoice parser. Users can upload invoice PDF files, extract product information, generate a CSV file, and download it directly from the web interface.

The application retrieves exchange rates from the BNR XML feed and calculates product prices in RON.

---

## Project Overview

This project was built as a technical task focused on:

- Web scraping
- Login-based automation
- Database persistence
- Flask web development
- Product CRUD operations
- PDF parsing
- CSV export
- Currency conversion
- Scheduled task execution

The scraper logs into a target website, extracts product information, and saves the data into a database.

The Flask interface allows users to:

- View all saved products
- Search products by title
- Edit product details
- Delete products
- Upload invoice PDFs
- Download extracted invoice data as CSV

For scraped products, the application stores the original price, currency, exchange rate, and price converted to RON.

---

## Features

### Web Scraping & Product Management

- Login-based web scraping using Playwright
- Product data extraction using BeautifulSoup
- SQL database integration using SQLAlchemy ORM
- Duplicate prevention using unique product titles
- Existing product update when scraped data changes
- Product price stored as numeric value
- Product currency storage
- Exchange rate retrieval from the BNR XML feed
- Automatic conversion of product prices to RON
- Price validation and parsing using Decimal
- Flask web interface for displaying products
- Product search by title
- Edit product functionality
- Delete product functionality
- Error display for invalid price input
- Basic CSS styling
- Environment variable configuration using `.env`
- Scheduled scraping using APScheduler

### PDF Invoice Processing

- PDF upload through Flask
- File validation for PDF uploads
- Secure filename handling using `secure_filename`
- Uploaded files saved with timestamp-based unique names
- PDF text extraction using pdfplumber
- Product line parsing using regular expressions
- CSV generation using pandas
- CSV download using Flask `send_file`

---

## Extracted Product Data From Website

For each scraped product, the application extracts and stores:

- Product title
- Product image URL
- Product description
- Product price
- Product currency
- Exchange rate
- Price converted to RON

The product price is extracted as text from the website, validated, converted to `Decimal`, and stored as a numeric value in the database.

---

## Extracted Product Data From Invoice PDF

For each product line found in the invoice PDF, the application extracts:

- Product code
- Product name
- Unit price
- Currency
- Quantity

Example CSV structure:

```csv
product_code,product_name,unit_price,currency,quantity
172812FXX,COMUTATOR PORNIRE FEBIXX,251.96,RON,-1
```

---

## Technologies Used

- Python
- Flask
- SQLAlchemy
- Playwright
- BeautifulSoup
- APScheduler
- pdfplumber
- pandas
- requests
- python-dotenv
- Werkzeug
- HTML
- CSS
- SQL database

---

## Project Structure

```text
web-products-scraper/
│
├── generated/
│
├── services/
│   ├── csv_generator.py
│   ├── exchange_rate_service.py
│   ├── pdf_parser.py
│   └── price_service.py
│
├── static/
│   ├── edit.css
│   ├── home.css
│   ├── invoices.css
│   └── products.css
│
├── templates/
│   ├── edit_product.html
│   ├── home.html
│   ├── products.html
│   └── upload_invoice.html
│
├── uploads/
│
├── .env.example
├── .gitignore
├── app.py
├── config.py
├── database.py
├── main.py
├── models.py
├── repository.py
├── requirements.txt
├── scheduler.py
├── scraper.py
└── README.md
```

---

## How It Works

### 1. Web Scraping

The scraper uses Playwright to open a browser, log into the target website, and access the products page.

After the page is loaded, BeautifulSoup parses the HTML and extracts product information.

The extracted data includes:

```text
title
image URL
description
price
currency
```

The scraper also handles pagination and continues scraping until there is no next page available.

---

### 2. Price Parsing & Currency Conversion

The scraped price is initially extracted as text.

The `price_service.py` module is responsible for:

```text
1. Validating the price input
2. Converting the price to Decimal
3. Calculating the price in RON
```

Invalid prices, such as empty values, non-numeric values, zero, or negative numbers, are rejected.

The `exchange_rate_service.py` module is responsible for:

```text
1. Requesting the BNR XML feed
2. Parsing the XML response
3. Finding the exchange rate for the product currency
4. Returning the exchange rate as Decimal
```

Example:

```text
price = 24.99
currency = USD
exchange_rate = current USD/RON rate
price_ron = price * exchange_rate
```

---

### 3. Database Storage

Products are stored in a SQL database using SQLAlchemy ORM.

The `Product` model contains:

```text
id
title
img
description
price
currency
exchange_rate
price_ron
```

The `title` field is unique, so duplicate products are avoided.

When the scraper finds a product that already exists, the application updates the existing record instead of inserting a duplicate.

The product price and price in RON are stored as numeric values using Decimal/Numeric types.

---

### 4. Flask Web Interface

The Flask application provides a simple interface where products can be viewed, searched, edited, and deleted.

Available routes:

```text
/
```

Displays the home page.

```text
/products
```

Displays all saved products.

```text
/products?search=<keyword>
```

Filters products by title.

```text
/products/<product_id>/edit
```

Allows editing an existing product.

When a product is edited, the application validates the price, retrieves the exchange rate again, and recalculates the price in RON.

If the price is invalid, an error message is displayed on the edit page.

```text
/products/<product_id>/delete
```

Deletes an existing product.

---

### 5. PDF Invoice Upload & CSV Export

The application includes a PDF invoice upload page.

Available route:

```text
/invoices/upload
```

The invoice processing flow is:

```text
Upload PDF
    ↓
Validate file extension
    ↓
Save PDF in uploads/
    ↓
Extract text using pdfplumber
    ↓
Parse product lines using regex
    ↓
Generate CSV using pandas
    ↓
Return CSV as download
```

Generated CSV files are saved in the `generated/` folder.

Uploaded PDF files are saved in the `uploads/` folder.

Both folders should be ignored by Git.

---

## Environment Variables

The application uses a `.env` file for configuration.

Create a `.env` file based on `.env.example`.

Example:

```env
CONNECTION_STRING_DB=database_url

BNR_URL=https://curs.bnr.ro/nbrfxrates.xml
BASE_PAGE_URL=https://www.web-scraping.dev
LOGIN_URL=https://www.web-scraping.dev/login

SCRAPER_USERNAME=your_username
SCRAPER_PASSWORD=your_password
```

Do not commit the real `.env` file to GitHub.

The repository should contain only:

```text
.env.example
```

---

## Installation

Clone the repository:

```bash
git clone <your-repository-url>
```

Navigate into the project folder:

```bash
cd web-products-scraper
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment on Windows:

```bash
.venv\Scripts\activate
```

Activate the virtual environment on macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Install Playwright browsers:

```bash
playwright install
```

Create a `.env` file based on `.env.example` and fill in the required values.

---

## requirements.txt

The project dependencies are:

```txt
flask
sqlalchemy
playwright
beautifulsoup4
python-dotenv
apscheduler
werkzeug
pdfplumber
pandas
requests
```

Depending on the database used, an additional driver may be required.

For PostgreSQL, for example:

```txt
psycopg2-binary
```

---

## Running the Scraper Manually

To run the scraper manually:

```bash
python main.py
```

This will:

```text
1. Start the scraper
2. Log in to the website
3. Extract product data
4. Retrieve exchange rates
5. Validate and convert product prices
6. Calculate product prices in RON
7. Save or update products in the database
```

---

## Running the Flask Application

To start the Flask web interface:

```bash
flask --app app run
```

For development mode:

```bash
flask --app app run --debug
```

Then open:

```text
http://127.0.0.1:5000/
```

Products page:

```text
http://127.0.0.1:5000/products
```

Invoice upload page:

```text
http://127.0.0.1:5000/invoices/upload
```

---

## Running the Scheduler

The project includes a scheduler using APScheduler.

The scheduler runs the scraper every hour between 12:00 and 18:00.

To start it:

```bash
python scheduler.py
```

The scheduler uses a cron-style trigger:

```text
Every day, every hour from 12:00 to 18:00, at minute 0.
```

---

## Running Flask and Scheduler Together

The Flask application and the scheduler can be run at the same time using two separate terminals.

Terminal 1:

```bash
flask --app app run --debug
```

Terminal 2:

```bash
python scheduler.py
```

The Flask app handles the user interface, while the scheduler handles automatic scraping.

---

## Main Application Flow

### Product scraping flow

```text
main.py
    ↓
scraper.py
    ↓
Logs into website and extracts products
    ↓
repository.py
    ↓
Validates price using price_service.py
    ↓
Gets exchange rate using exchange_rate_service.py
    ↓
Calculates price in RON
    ↓
Saves or updates products in database
    ↓
app.py
    ↓
Displays products in Flask web interface
```

### Invoice processing flow

```text
PDF upload
    ↓
services/pdf_parser.py
    ↓
Extracts product data from invoice PDF
    ↓
services/csv_generator.py
    ↓
Generates CSV file
    ↓
Flask send_file
    ↓
Downloads CSV in browser
```

---

## Current Functionalities

- Scrape products from the target website
- Log in before scraping
- Handle product pagination
- Save products into the database
- Prevent duplicate products by title
- Update existing products when scraped data changes
- Store product price as numeric value
- Store product currency
- Retrieve exchange rates from BNR XML
- Convert product prices to RON
- Validate price input
- Display products in a web page
- Search products by title
- Edit existing products
- Show validation errors on edit
- Recalculate RON price after product edit
- Delete existing products
- Schedule automatic scraping
- Upload invoice PDF files
- Extract product data from PDF invoices
- Generate CSV files from extracted invoice data
- Download generated CSV files from the browser

---

## Git Ignore Notes

The repository should not include sensitive or generated files.

Recommended `.gitignore` entries:

```gitignore
.venv/
__pycache__/
*.pyc

.env

uploads/*
generated/*
```

If you want to keep the `uploads/` and `generated/` folders in Git without committing their contents, add an empty `.gitkeep` file inside each folder and use:

```gitignore
uploads/*
!uploads/.gitkeep

generated/*
!generated/.gitkeep
```

---

## Future Improvements

Possible improvements for this project:

- Add flash messages after edit, delete, and upload actions
- Add stronger validation for uploaded PDF files
- Add error handling for unsupported invoice formats
- Add logging instead of simple terminal output
- Add pagination in the Flask product interface
- Add advanced sorting and filtering
- Improve exchange rate caching
- Add Docker support
- Add unit tests for price parsing, repository logic, PDF parsing, and exchange rate retrieval
- Rename `main.py` to `run_scraper.py` for better clarity
- Deploy the application online