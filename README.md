# Web Products Scraper & Invoice Parser

A Python web application that authenticates on a target website, scrapes product data, stores it in a SQL database, and provides a simple Flask interface for product management.

The project also includes a PDF invoice parser that allows users to upload invoice PDFs, extract product information, generate a CSV file, and download it directly from the web interface.

Additionally, the application retrieves exchange rates from the BNR XML feed and calculates product prices in RON.

## Project Overview

This project was built as a technical task focused on:

- Web scraping
- Database persistence
- Scheduled task execution
- Flask web interface development
- PDF parsing
- CSV export
- Currency conversion to RON

The application logs into a target website, extracts product information, and stores it in a database. The saved products can be viewed, searched, edited, and deleted through a Flask interface.

Invoice PDF files can also be uploaded through the web application. The system extracts product data from the invoice and exports it as a CSV file.

For scraped products, the application stores the original price and currency, retrieves the daily exchange rate, calculates the price in RON, and saves the result in the database.

## Features

### Web Scraping & Product Management

- Login-based web scraping using Playwright
- Product data extraction using BeautifulSoup
- SQL database integration using SQLAlchemy ORM
- Duplicate prevention using unique product titles
- Existing product update when scraped data changes
- Product price and currency storage
- Exchange rate retrieval from BNR XML
- Automatic conversion of product prices to RON
- Flask web interface for displaying products
- Product search by title
- Edit product functionality
- Delete product functionality
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

## Extracted Product Data From Website

For each scraped product, the application extracts and stores:

- Product title
- Product image URL
- Product price
- Product currency
- Product description
- Exchange rate
- Price converted to RON

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
- HTML
- CSS
- SQL database

## Project Structure

```text
web-products-scraper/
│
├── generated/
│
├── services/
│   ├── csv_generator.py
│   ├── exchange_rate_service.py
│   └── pdf_parser.py
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
├── database.py
├── main.py
├── models.py
├── repository.py
├── requirements.txt
├── scheduler.py
├── scraper.py
└── README.md
```

## How It Works

### 1. Web Scraping

The scraper uses Playwright to open a browser, authenticate on the website, and access the products page.

After the page is loaded, BeautifulSoup is used to parse the HTML and extract product information.

The extracted data includes:

```text
title
image URL
description
price
currency
```

The product currency is stored separately from the price so that exchange rate conversion can be performed.

### 2. Database Storage

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

During save/update, the application retrieves the exchange rate for the product currency and calculates the price in RON.

### 3. Currency Conversion

The application retrieves exchange rates from the BNR XML feed.

The exchange rate service:

```text
1. Requests the BNR XML file
2. Parses the XML using ElementTree
3. Finds the rate matching the product currency
4. Returns the exchange rate as Decimal
5. Calculates the product price in RON
```

For example:

```text
price = 24.99
currency = USD
exchange_rate = current USD/RON rate
price_ron = price * exchange_rate
```

If the currency is already RON, the exchange rate is treated as `1`.

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

When a product is edited, the application recalculates the exchange rate and price in RON based on the updated price and currency.

```text
/products/<product_id>/delete
```

Deletes an existing product.

### 5. PDF Invoice Upload & CSV Export

The application also includes a PDF invoice upload page.

Available route:

```text
/invoices/upload
```

The invoice processing flow is:

```text
Upload PDF
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

Both folders are ignored by Git.

## Environment Variables

The application uses a `.env` file for configuration.

Create a `.env` file based on `.env.example`.

Example:

```env
BASE_PAGE_URL=https://www.web-scraping.dev
LOGIN_URL=https://www.web-scraping.dev/login
SCRAPER_USERNAME=your_username
SCRAPER_PASSWORD=your_password
BNR_URL=https://www.bnr.ro/nbrfxrates.xml
DATABASE_URL=your_database_url
```

Do not commit the real `.env` file to GitHub.

The repository should contain only:

```text
.env.example
```

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

Activate the virtual environment:

```bash
.venv\Scripts\activate
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
5. Calculate product prices in RON
6. Save or update products in the database
```

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
http://127.0.0.1:5000/products
```

To access the invoice upload page:

```text
http://127.0.0.1:5000/invoices/upload
```

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

## requirements.txt

The project dependencies should include:

```txt
flask
sqlalchemy
playwright
beautifulsoup4
python-dotenv
apscheduler
pdfplumber
pandas
requests
```

Depending on the database used, an additional driver may be required.

For PostgreSQL, for example:

```txt
psycopg2-binary
```

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

This keeps uploaded PDFs and generated CSV files out of GitHub.

## Main Application Flow

```text
scraper.py
    ↓
Extracts products from website
    ↓
exchange_rate_service.py
    ↓
Retrieves exchange rates and calculates price in RON
    ↓
repository.py
    ↓
Saves or updates products in database
    ↓
app.py
    ↓
Displays products in Flask web interface
```

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

## Current Functionalities

- Scrape products from the target website
- Save products into the database
- Prevent duplicate products by title
- Update existing products when scraped data changes
- Store original price and currency
- Retrieve exchange rates from BNR XML
- Convert product prices to RON
- Display products in a web page
- Search products by title
- Edit existing products
- Recalculate RON price after product edit
- Delete existing products
- Schedule automatic scraping
- Upload invoice PDF files
- Extract product data from PDF invoices
- Generate CSV files from extracted invoice data
- Download generated CSV files from the browser

## Future Improvements

Possible improvements for this project:

- Add better flash messages after edit/delete/upload actions
- Add stronger validation for uploaded PDF files
- Add error handling for unsupported invoice formats
- Add logging instead of simple terminal output
- Add pagination in the Flask product interface
- Add advanced sorting and filtering
- Add caching for exchange rates per scraping run
- Add Docker support
- Add unit tests for repository, parser, and exchange rate service functions
- Deploy the application online