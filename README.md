# Web Products Scraper

A Python application that authenticates on a web scraping practice website, extracts product data, stores it in a SQL database, and provides a simple Flask web interface for viewing, editing, and deleting the saved products.

## Project Overview

This project was built as a technical task focused on web scraping, database persistence, scheduled execution, and basic web interface development.

The application logs into the target website, accesses the products page, extracts product information, and saves it into a database. The saved products can then be managed through a simple Flask interface.

## Features

- Login-based web scraping using Playwright
- Product data extraction using BeautifulSoup
- SQL database integration using SQLAlchemy ORM
- Product storage with duplicate prevention
- Product update when existing data changes
- Flask web interface for displaying products
- Edit product functionality
- Delete product functionality
- Basic CSS styling
- Environment variable configuration using `.env`
- Periodic scraper execution using APScheduler
- Alternative scheduling support using Windows Task Scheduler

## Extracted Product Data

For each product, the scraper extracts:

- Product title
- Product image URL
- Product price
- Product description

## Technologies Used

- Python
- Flask
- SQLAlchemy
- Playwright
- BeautifulSoup
- APScheduler
- python-dotenv
- HTML
- CSS
- SQL database

## Project Structure

```text
web-products-scraper/
│
├── static/
│   └── products.css
│   ├── edit.css
│
├── templates/
│   ├── home.html
│   ├── products.html
│   └── edit_product_page.html
│
├── .env
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

### 1. Scraping

The scraper uses Playwright to open a browser, authenticate on the website, and access the products page.

After the page is loaded, BeautifulSoup is used to parse the HTML and extract product information.

The scraper collects data such as:

```text
title
image URL
description
price
```

### 2. Database Storage

Products are stored in a SQL database using SQLAlchemy ORM.

The `Product` model contains the following fields:

```text
id
title
img
description
price
```

The `title` field is unique, so the application avoids inserting duplicate products.

If a product already exists, its information can be updated instead of creating a duplicate entry.

### 3. Web Interface

The Flask application provides a simple interface where products can be viewed, edited, and deleted.

Available pages:

```text
/
```
Home root

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

## Environment Variables

The application uses a `.env` file for configuration.

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

## Running the Scraper Manually

To run the scraper manually:

```bash
python main.py
```

This will:

```text
1. Start the scraper
2. Login to the website
3. Extract product data
4. Save or update products in the database
```

## Running the Flask Application

To start the Flask web interface:

```bash
flask --app app run --debug
```

Then open:

```text
http://127.0.0.1:5000/products
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

## Windows Task Scheduler Alternative

The scraper can also be scheduled using Windows Task Scheduler.

Recommended setup:

```text
Trigger:
Daily
Start: 12:00 PM
Repeat every: 1 hour
Duration: 7 hours
```

Action:

```text
Program/script:
path\to\.venv\Scripts\python.exe

Add arguments:
main.py

Start in:
path\to\project-folder
```

This allows Windows to run the scraper automatically without keeping `scheduler.py` open.

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

## Current Functionalities

- Scrape products from the target website
- Save products into the database
- Prevent duplicate products by title
- Display products in a web page
- Edit existing products
- Delete existing products
- Schedule automatic scraping

## Notes

The Flask application and the scheduler can be run at the same time using two separate terminals:

```bash
flask --app app run --debug
```

```bash
python scheduler.py
```

The Flask app handles the user interface, while the scheduler handles automatic scraping.
