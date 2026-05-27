from sqlalchemy import create_engine

from config import DATABASE_URL
from models import Base


engine = create_engine(DATABASE_URL, echo=True) # connection SQLAlchemy with PostgreSQL

Base.metadata.create_all(engine) # creates all table based on models
