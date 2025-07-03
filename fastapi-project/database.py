from fastapi import FastAPI,Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm   
from passlib.context import CryptContext 
from jose import JWTError
from jose import jwt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,DeclarativeBase, Session
from typing import Annotated
from fastapi import HTTPException, Cookie
from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi import Request, Response
import uuid
from datetime import datetime, timedelta
import os
from .models import Base, CustomerDB, OrderDB

DB_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
session = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base.metadata.create_all(bind=engine)
def get_database():
    db = session()
    try:
        yield db
    finally:
        db.close()


SessionDep = Annotated[Session, Depends(get_database)]

