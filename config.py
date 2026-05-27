import os
from dotenv import load_dotenv

load_dotenv()

ALLOWED_EXTENSIONS = {'pdf'}
PRODUCTS_PATH = "/products?category=consumables"
DEFAULT_CURRENCY = "USD"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
GENERATED_FOLDER = os.path.join(BASE_DIR, "generated")


def get_env_value(name):
    value = os.getenv(name)

    if not value:
        raise ValueError(f"Missing required env variable: {name}")

    return value


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


ADMIN_USERNAME = get_env_value("ADMIN_USERNAME")
ADMIN_PASSWORD = get_env_value("ADMIN_PASSWORD")
SESSION_SECRET_KEY = get_env_value("SECRET_KEY")

BASE_PAGE_URL = get_env_value("BASE_PAGE_URL")
LOGIN_URL = get_env_value("LOGIN_URL")
PAGE_USERNAME = get_env_value("SCRAPER_USERNAME")
PAGE_PASSWORD = get_env_value("SCRAPER_PASSWORD")

DATABASE_URL = get_env_value("CONNECTION_STRING_DB")

BNR_URL = get_env_value("BNR_URL")
