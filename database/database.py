import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Load environment variables
load_dotenv()

# RDS MySQL connection details
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

SQLALCHEMY_DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Production-ready MySQL engine (no SQLite-specific args)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,           # Validates connections before use
    pool_recycle=3600,            # Recycle connections every hour
    pool_size=int(os.getenv("DB_POOL_SIZE", 10)),
    max_overflow=int(os.getenv("DB_MAX_OVERFLOW", 20))
)

# sessionlocal = sessionmaker(autocommit=True, autoflush=True, bind=engine)
sessionlocal = sessionmaker(autoflush=True, bind=engine)
Base = declarative_base()