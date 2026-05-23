import os
from playwright.sync_api import sync_playwright
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from dotenv import load_dotenv


load_dotenv()


def get_env_value(name):
    value = os.getenv(name)

    if not value:
        raise ValueError(f"Missing required env variable: {name}")

    return value

BASE_PAGE_URL = get_env_value("BASE_PAGE_URL")
LOGIN_URL = get_env_value("LOGIN_URL")
USERNAME = get_env_value("SCRAPER_USERNAME")
PASSWORD = get_env_value("SCRAPER_PASSWORD")


def scrape_products() -> list[dict]:
    products_data = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=100)
        page = browser.new_page()

        page.goto(LOGIN_URL)
        page.get_by_placeholder("user123").fill(USERNAME)
        page.get_by_placeholder("password").fill(PASSWORD)

        page.get_by_role("button", name="Submit").click()
        page.wait_for_timeout(1000)  # for safe loading

        current_url = urljoin(BASE_PAGE_URL, "/products")

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

                img = urljoin(BASE_PAGE_URL, img_relative)

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

            current_url = urljoin(BASE_PAGE_URL, str(next_href))
        browser.close()

    return products_data