import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

if "pytest" not in sys.modules:
    SQLALCHEMY_DATABASE_URL = "sqlite:///testing.db"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL
    )


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
