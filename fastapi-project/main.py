from fastapi import FastAPI,Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm   
from passlib.context import CryptContext 
from jose import jwt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,DeclarativeBase, Session
from .schema import CustomerCreate, Customer,CustomerPatch
from .models import Base,CustomerDB
from typing import Annotated
from fastapi import HTTPException, Cookie
from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi import Request, Response
import uuid
import os
from dotenv import load_dotenv
from fastapi.routing import APIRouter
from datetime import datetime, timedelta
from .database import get_database, SessionDep
load_dotenv()
from .constants import SECRET_KEY, ALGORITHM
from .authentication import oauth2_scheme, create_access_token, get_current_user
from .routs.customer import router_customer
from .routs.token import token_router



app = FastAPI()
# DB_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")  # Default to SQLite for testing
# from fastapi import FastAPI
# from contextlib import asynccontextmanager
# from .database import engine, SessionLocal
# from .models import Base

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # Startup: create tables
#     Base.metadata.create_all(bind=engine)
#     print("Database tables created")
#     yield
#     # Shutdown: dispose engine
#     engine.dispose()
#     print("Database engine disposed")

# def get_database():
#     db = session()
#     try:
#         yield db
#     finally:
#         db.close()

# router = APIRouter(prefix="/api", tags=["api"])

# # engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
# # session = sessionmaker(bind=engine, autocommit=False, autoflush=False)
# # Base.metadata.create_all(bind=engine)
# # SessionDep = Annotated[Session, Depends(get_database)]

# session_store = {}



# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")        
# SECRET_KEY = "your-secret-key"  # Use a secure random key in production!
# ALGORITHM = "HS256"

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto") # This should be replaced with a proper hashing mechanism
# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)
# def get_password_hash(password):
#     return pwd_context.hash(password)

# def create_access_token(data: dict, expires_delta: int = 3600):
#     # This function should create a JWT token     
#     expires = datetime.now() + timedelta(seconds=expires_delta)  
#     #data.update({"exp": expires})
#     return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

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

# def get_current_user(
#     db: SessionDep ,
#     #token: str = Depends(oauth2_scheme),
#     session_id: str = Cookie(None)
# ):
    
#     # if token:
#     #     try:
#     #         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#     #         email: str = payload.get("sub")
#     #         if email is None:
#     #             raise HTTPException(status_code=401, detail="Invalid JWT token")
#     #         user = db.query(CustomerDB).filter(CustomerDB.email == email).first()
#     #         if not user:
#     #             raise HTTPException(status_code=401, detail="User not found")
#     #         return user
#     #     except JWTError:
#     #         pass  # If JWT fails, try session cookie

#     if session_id or session_id in session_store:
#         email = session_store[session_id]
#         print(f"Session ID: {session_id}, Email: {email}")
#         user = db.query(CustomerDB).filter(CustomerDB.email == email).first()
#         if user:
#             return user

#     raise HTTPException(status_code=401, detail="Not authenticated")


@app.get("/")
def read_root():
    return {"Hello": "World"}

# @app.post("/customer", response_model=Customer)
# def customer(customer: CustomerCreate, db: SessionDep):
#     #db_customer = CustomerDB(name=customer.name, email=customer.email)
#     if db.query(CustomerDB).filter(CustomerDB.email == customer.email).first():
#         return {"error": "Email already registered"}
#     hashed_password = get_password_hash(customer.password)  # Hash the password
#     print(customer.model_dump())
#     # Create a new customer instance    
#     db_customer = CustomerDB(
#         **customer.model_dump(exclude={"password"}),  # Exclude password from the model dump
#         password_hash=hashed_password)
#     db.add(db_customer)
#     db.commit()
#     db.refresh(db_customer)
#     return db_customer
# Current_user_DP = Annotated[CustomerDB, Depends(get_current_user)]

# @app.put("/customer/{customer_id}", response_model=Customer, )
# def update_customer(customer_id: int, customer: CustomerCreate, db: SessionDep, current_user: CustomerDB = Depends(get_current_user)):
#     db_customer = db.query(CustomerDB).filter(CustomerDB.id == customer_id).first()
#     print(customer_id, customer, db_customer)
#     if not db_customer:
#         return {"error": "Customer not found"}
    
#     for key, value in customer.model_dump().items():
#         setattr(db_customer, key, value)
    
#     db.commit()
#     db.refresh(db_customer)
#     return db_customer

# @app.patch("/customer/{customer_id}", response_model=Customer)
# def patch_customer(customer_id: int, customer: CustomerPatch, db: SessionDep):
#     db_customer = db.query(CustomerDB).filter(CustomerDB.id == customer_id).first()
#     if not db_customer:
#         return {"error": "Customer not found"}
#     print(db_customer.email,db_customer.name,customer.model_dump(exclude_none=True))
#     setattr(db_customer.email,db_customer.name, customer.model_dump(exclude_none=True).items())
#     # for key, value in customer.model_dump().items():
#     #     if value is not None:
#     #         setattr(db_customer, key, value)
#     db.commit()
#     db.refresh(db_customer)
#     return db_customer

# @app.get("/customer/{customer_id}", response_model=Customer) #123
# def get_customer(customer_id: int, db: SessionDep,current_user: CustomerDB = Depends(get_current_user)):
#     customer = db.query(CustomerDB).filter(CustomerDB.id == customer_id).first()
#     if not customer:
#         return {"error": "Customer not found"}
    
#     print(customer.password_hash)
#     return customer



# @app.get("/customers",response_model=list[Customer])
# def list_customer(db:SessionDep, current_user: CustomerDB = Depends(get_current_user)):
#     customers = db.query(CustomerDB).all()
#     return customers

# @app.post("/token")
# def login(db: SessionDep,form_data: OAuth2PasswordRequestForm = Depends()):
#     #db = SessionDep()
#     user = db.query(CustomerDB).filter(CustomerDB.email == form_data.username).first()
#     if not user or not verify_password(form_data.password, user.password_hash):
#         return {"error": "Invalid credentials"}
    
#     access_token = create_access_token(data={"sub": user.email})
#     return {"access_token": access_token, "token_type": "bearer"}

# @app.post("/login")
# def login(
#     db: SessionDep ,
#     response: Response,
#     form_data: OAuth2PasswordRequestForm = Depends(),
    
# ):
#     user = db.query(CustomerDB).filter(CustomerDB.email == form_data.username).first()
#     if not user or not verify_password(form_data.password, user.password_hash):
#         raise HTTPException(status_code=401, detail="Invalid credentials")
#     # JWT token
#     access_token = create_access_token(data={"sub": user.email})
#     # Session cookie
#     session_id = str(uuid.uuid4())
#     session_store[session_id] = user.email
    
#     print(session_store) #Redis or any other storage can be used here
#     response.set_cookie(
#         key="session_id",
#         value=session_id, #47cd039a-94c3-42a4-9920-84b64887ad5c - 7ecd8023-e602-4394-8eee-68f0d1de88d8
#         httponly=True,
#         max_age=60*60*24,
#         samesite="lax",
#         secure=False  # Set to True in production
#     )
#     return {"access_token": access_token, "token_type": "bearer", "session_id": session_id}


app.include_router(router_customer)
app.include_router(token_router)  # Removed because token_router is not defined