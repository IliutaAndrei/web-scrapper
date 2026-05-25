import re
import pdfplumber

def parse_product_line(line):
    pattern = r"^\d+\s+(\S+)\s+(.+?)\s+(-?\d+(?:\.\d+)?)\s+([A-Z]{3})\s+(-?\d+(?:\.\d+)?)"

    match = re.search(pattern, line)

    if not match:
        return None

    return {
        "product_code": match.group(1),
        "product_name": match.group(2),
        "unit_price": match.group(3),
        "currency": match.group(4),
        "quantity": match.group(5)
    }


def extract_products_from_pdf(pdf_path):
    products = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()

            if not text:
                continue

            lines = text.split("\n")

            for line in lines:
                product = parse_product_line(line)

                if product:
                    products.append(product)

    return products

