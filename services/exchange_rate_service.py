import requests
import xml.etree.ElementTree as ET
from decimal import Decimal

from config import BNR_URL


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

