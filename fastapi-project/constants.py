import os
from dotenv import load_dotenv  
load_dotenv()
from passlib.context import CryptContext
import redis

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")  # Use a secure random key in production!
ALGORITHM = os.getenv("ALGORITHM")

#session_store = {}
session_store = redis.Redis(host = "localhost",port=6379, db=0,decode_responses = True)  # This will hold session data in memory for simplicity
pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")