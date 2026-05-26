import os
from dotenv import load_dotenv

load_dotenv()

def get_env_value(name):
    value = os.getenv(name)

    if not value:
        raise ValueError(f"Missing required env variable: {name}")

    return value

PRODUCTS_PATH = "/products"
DEFAULT_CURRENCY = "USD"

BASE_PAGE_URL = get_env_value("BASE_PAGE_URL")
LOGIN_URL = get_env_value("LOGIN_URL")
PAGE_USERNAME = get_env_value("SCRAPER_USERNAME")
PAGE_PASSWORD = get_env_value("SCRAPER_PASSWORD")

BNR_URL = get_env_value("BNR_URL")