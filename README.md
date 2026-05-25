# Web Products Scraper & Invoice Parser

A Python web application that authenticates on a target website, scrapes product data, stores it in a SQL database, and provides a simple Flask interface for product management.

The project also includes a PDF invoice parser that allows users to upload invoice PDFs, extract product information, generate a CSV file, and download it directly from the web interface.

## Project Overview

This project was built as a technical task focused on:

- Web scraping
- Database persistence
- Scheduled task execution
- Flask web interface development
- PDF parsing
- CSV export

The application logs into a target website, extracts product information, and stores it in a database. The saved products can be viewed, edited, and deleted through a Flask interface.

Additionally, invoice PDF files can be uploaded through the web application. The system extracts product data from the invoice and exports it as a CSV file.

## Features

### Web Scraping & Product Management

- Login-based web scraping using Playwright
- Product data extraction using BeautifulSoup
- SQL database integration using SQLAlchemy ORM
- Duplicate prevention using unique product titles
- Existing product update when scraped data changes
- Flask web interface for displaying products
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

For each scraped product, the application extracts:

- Product title
- Product image URL
- Product price
- Product description

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
- python-dotenv
- HTML
- CSS
- SQL database

## Project Structure

```text
web-products-scraper/
│
├── generated/
│   └── .gitkeep
│
├── services/
│   ├── csv_generator.py
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
│   └── .gitkeep
│
├── .env.example
├── .gitignore
├── app.py
├── database.py
├── main.py
├── models.py
├── repository.py
├── scraper.py
├── scheduler.py
├── requirements.txt
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
```

### 2. Database Storage

Products are stored in a SQL database using SQLAlchemy ORM.

The `Product` model contains:

```text
id
title
img
description
price
```

The `title` field is unique, so duplicate products are avoided.

When the scraper finds a product that already exists, the application updates the existing record instead of inserting a duplicate.

### 3. Flask Web Interface

The Flask application provides a simple interface where products can be viewed, edited, and deleted.

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
/products/<product_id>/edit
```

Allows editing an existing product.

```text
/products/<product_id>/delete
```

Deletes an existing product.


### 4. PDF Invoice Upload & CSV Export

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

Both folders are ignored by Git, except for `.gitkeep` files used to preserve the folder structure.

## Environment Variables

The application uses a `.env` file for configuration.

Create a `.env` file based on `.env.example`.

Example:

```env
BASE_PAGE_URL=https://www.web-scraping.dev
LOGIN_URL=https://www.web-scraping.dev/login
SCRAPER_USERNAME=your_username
SCRAPER_PASSWORD=your_password
DATABASE_URL=your_database_url
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
4. Save or update products in the database
```

## Running the Flask Application

To start the Flask web interface:

```bash
flask --app app run 
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
```

Depending on the database used, an additional driver may be required.

For PostgreSQL, for example:

```txt
psycopg2-binary
```


## Main Application Flow

```text
scraper.py
    ↓
Extracts products from website
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
- Display products in a web page
- Edit existing products
- Delete existing products
- Schedule automatic scraping
- Upload invoice PDF files
- Extract product data from PDF invoices
- Generate CSV files from extracted invoice data
- Download generated CSV files from the browser

## Future Improvements

Possible improvements for this project:

- Add flash messages after edit/delete/upload actions
- Add stronger validation for uploaded PDF files
- Add error handling for unsupported invoice formats
- Add logging instead of simple terminal output
- Add pagination in the Flask product interface
- Add Docker support
- Add unit tests for repository and parser functions