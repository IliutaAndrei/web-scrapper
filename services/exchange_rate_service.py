import requests
from dotenv import load_dotenv
import xml.etree.ElementTree as ET
from decimal import Decimal
from scraper import get_env_value

load_dotenv()

BNR_URL = get_env_value("BNR_URL")

def get_price_in_ron(price, exchange_rate):
    price_value = Decimal(price)
    price_ron = price_value * exchange_rate

    return price_ron.quantize(Decimal("0.01"))


def get_exchange_rate(currency):
    response = requests.get(BNR_URL)
    response.raise_for_status()

    xml_text = response.text
    root = ET.fromstring(xml_text)

    for element in root.iter():
        if element.attrib.get("currency") == currency:
            rate_text = element.text
            if not rate_text:
                return None
            return Decimal(rate_text)
    return None


