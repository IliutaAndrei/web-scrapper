import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

load_dotenv()

DATABASE_URL = os.getenv("CONNECTION_STRING_DB")

if not DATABASE_URL:
    raise ValueError("CONNECTION_STRING_DB is missing from .env")

engine = create_engine(DATABASE_URL, echo=True) # connection SQLAlchemy with PostgreSQL
SessionLocal = sessionmaker(bind=engine) # db session

Base.metadata.create_all(engine) # creates all table based on models
