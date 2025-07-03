import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from dotenv import load_dotenv
from typing import Annotated
from fastapi import Depends

# Load environment variables from .env file
load_dotenv()

# Database URL from environment variable
DATABASE_URL = os.getenv("DB_URL")
if not DATABASE_URL:
    raise RuntimeError("DB_URL environment variable not set")

# SQLAlchemy engine and session configuration
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # Only needed for SQLite
)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)



# Dependency for getting DB session
def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

sessionDep = Annotated[session, Depends(get_db)]