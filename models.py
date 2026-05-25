from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Text, Numeric

from decimal import Decimal

class Base(DeclarativeBase):
    pass

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=True, nullable=False)
    img: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    price: Mapped[str] = mapped_column(nullable=False)
    currency: Mapped[str] = mapped_column(nullable=False)
    exchange_rate: Mapped[Decimal] = mapped_column(Numeric(10,4), nullable=False)
    price_ron: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

