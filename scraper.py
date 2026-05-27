from config import LOGIN_URL, PAGE_USERNAME, PAGE_PASSWORD, BASE_PAGE_URL, PRODUCTS_PATH, DEFAULT_CURRENCY
from playwright.sync_api import sync_playwright, Page
from urllib.parse import urljoin
from bs4 import BeautifulSoup


def get_next_page_url(soup: BeautifulSoup, base_url: str) -> str | None:
    paging_links = soup.select("div.paging a")
    next_link = None

    for link in paging_links:
        if link.get_text(strip=True) == ">":
            next_link = link
            break

    if not next_link:
        return None

    next_href = next_link.get("href")

    if not next_href:
        return None

    return urljoin(base_url, str(next_href))

def extract_product_data(product, currency: str, base_url: str) -> dict | None:
    title_element = product.select_one("div.description > h3 > a")
    img_element = product.select_one("img.img-thumbnail")
    desc_element = product.select_one("div.short-description")
    price_element = product.select_one("div.price")

    if not title_element or not img_element or not desc_element or not price_element:
        return None

    title = title_element.get_text(strip=True)
    img_relative = str(img_element.get("src", ""))
    desc = desc_element.get_text(strip=True)
    price = price_element.get_text(strip=True)

    if not img_relative:
        return None

    img = urljoin(base_url, img_relative)

    return {
        "title": title,
        "img": img,
        "description": desc,
        "price": price,
        "currency": currency
    }


def login(page: Page , login_url: str, username: str, password: str):
    page.goto(login_url)

    username_element = page.get_by_placeholder("user123")
    password_element = page.get_by_placeholder("password")
    submit_element = page.get_by_role("button", name="Submit")

    username_element.fill(username)
    password_element.fill(password)
    submit_element.click()

    page.wait_for_timeout(1000) #for safe loading



def scrape_products() -> list[dict]:
    products_data = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, slow_mo=100)
        page = browser.new_page()

        login(page, LOGIN_URL, PAGE_USERNAME, PAGE_PASSWORD)

        current_url = urljoin(BASE_PAGE_URL, PRODUCTS_PATH)
        currency = DEFAULT_CURRENCY

        while True:
            page.goto(current_url)

            html = page.content()
            soup = BeautifulSoup(html, "html.parser")

            products = soup.select("div.product")

            for product in products:
                product_data = extract_product_data(product, currency, BASE_PAGE_URL)

                if product_data:
                    products_data.append(product_data)

            next_page_url = get_next_page_url(soup, BASE_PAGE_URL)

            if not next_page_url:
                break

            current_url = next_page_url
        browser.close()

    return products_data