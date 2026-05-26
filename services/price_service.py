from decimal import Decimal, InvalidOperation

def get_price_in_ron(price: Decimal, exchange_rate: Decimal) -> Decimal:
    price_ron = price * exchange_rate

    return price_ron.quantize(Decimal("0.01"))



def parse_price(price: str) -> Decimal:
    if not price:
        raise ValueError("Price is required")

    price = price.strip()

    if not price:
        raise ValueError("Price is required")

    try:
        price_value = Decimal(price)
    except InvalidOperation:
        raise ValueError("Price must be a valid number")

    if price_value < 0:
        raise ValueError("Price must be greater than 0")

    return price_value.quantize(Decimal("0.01"))