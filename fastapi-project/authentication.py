from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from datetime import datetime, timedelta
import os
from .constants import SECRET_KEY, ALGORITHM,session_store

from passlib.context import CryptContext  # Add this import
from fastapi import HTTPException, Cookie  # Add this import

# Import Session from SQLAlchemy and define SessionDep if not already defined
from sqlalchemy.orm import Session
from .models import CustomerDB
from .database import SessionDep

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  # Add this line

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict, expires_delta: int = 3600):
    # This function should create a JWT token     
    expires = datetime.now() + timedelta(seconds=expires_delta)  
    #data.update({"exp": expires})
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
def get_password_hash(password):
    return pwd_context.hash(password)

def get_current_user(
    db: SessionDep ,
    #token: str = Depends(oauth2_scheme),
    session_id: str = Cookie(None)
):
    
    # if token:
    #     try:
    #         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    #         email: str = payload.get("sub")
    #         if email is None:
    #             raise HTTPException(status_code=401, detail="Invalid JWT token")
    #         user = db.query(CustomerDB).filter(CustomerDB.email == email).first()
    #         if not user:
    #             raise HTTPException(status_code=401, detail="User not found")
    #         return user
    #     except JWTError:
    #         pass  # If JWT fails, try session cookie

    if session_id: #or session_id in session_store:
        #email = session_store[session_id]
        print(session_store.keys('session:*'))
        email = session_store.get(f"session:{session_id}")
        print(f"Session ID: {session_id}, Email: {email}")
        user = db.query(CustomerDB).filter(CustomerDB.email == email).first()
        if user:
            return user

    raise HTTPException(status_code=401, detail="Not authenticated")

# def get_current_user(db: SessionDep,token: str = Depends(oauth2_scheme)):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         print(payload)
#         email: str = payload.get("sub")
#         if email is None:
#             raise Exception("Invalid authentication credentials")
#         user = db.query(CustomerDB).filter(CustomerDB.email == email).first()
#         if user is None:
#             raise Exception("User not found")
#         return user
#     except jwt.JWTError:
#         raise Exception("Invalid authentication credentials")