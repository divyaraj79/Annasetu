from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.models import *

DATABASE_URL = "YOUR_DATABASE_URL"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
