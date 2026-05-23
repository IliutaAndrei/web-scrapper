from playwright.sync_api import sync_playwright
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from database import SessionLocal
from models import Product

base_page_url = "https://www.web-scraping.dev"
login_url = "https://www.web-scraping.dev/login"

products_data = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=100)
    page = browser.new_page()

    page.goto(login_url)
    page.get_by_placeholder("user123").fill("user123")
    page.get_by_placeholder("password").fill("password")

    page.get_by_role("button", name="Submit").click()
    page.wait_for_timeout(1000)  # for safe loading

    current_url = urljoin(base_page_url, "/products")

    while True:
        page.goto(current_url)

        html = page.content()
        soup = BeautifulSoup(html, "html.parser")

        products = soup.select("div.product")

        for product in products:
            title_element = product.select_one("div.description > h3 > a")
            img_element = product.select_one("img.img-thumbnail")
            desc_element = product.select_one("div.short-description")
            price_element = product.select_one("div.price")

            if not title_element or not img_element or not desc_element or not price_element:
                continue

            title = title_element.get_text(strip=True)
            img_relative = str(img_element.get("src", ""))
            desc = desc_element.get_text(strip=True)
            price = price_element.get_text(strip=True)

            if not img_relative:
                continue

            img = urljoin(base_page_url, img_relative)

            product_data = {
                "title": title,
                "img": img,
                "description": desc,
                "price": price
            }

            products_data.append(product_data)

        paging_links = soup.select("div.paging a")
        next_link = None

        for link in paging_links:
            if link.get_text(strip=True) == ">":
                next_link = link
                break

        if not next_link:
            break

        next_href = next_link.get("href")

        if not next_href:
            break

        current_url = urljoin(base_page_url, str(next_href))

with SessionLocal() as session:
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
