from fastapi import FastAPI,Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,DeclarativeBase, Session
from .models import CustomerCreate, OrderCreate, Customer, Order,CustomerDB, OrderDB, Base,CustomerPatch
from typing import Annotated

from fastapi.routing import APIRouter

app = FastAPI()
DB_URL = "sqlite:///./test.db"
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

def get_database():
    db = session()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(prefix="/api", tags=["api"])

engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
session = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base.metadata.create_all(bind=engine)
SessionDep = Annotated[Session, Depends(get_database)]
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm   
from passlib.context import CryptContext 
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")      
SECRET_KEY = "your-secret-key"  # Use a secure random key in production!
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto") # This should be replaced with a proper hashing mechanism
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
def get_password_hash(password):
    return pwd_context.hash(password)
def create_access_token(data: dict):
    # This function should create a JWT token       
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/customer", response_model=Customer)
def customer(customer: CustomerCreate, db: SessionDep):
    #db_customer = CustomerDB(name=customer.name, email=customer.email)
    if db.query(CustomerDB).filter(CustomerDB.email == customer.email).first():
        return {"error": "Email already registered"}
    hashed_password = get_password_hash(customer.password)  # Hash the password
    print(customer.model_dump())
    # Create a new customer instance    
    db_customer = CustomerDB(
        **customer.model_dump(exclude={"password"}),  # Exclude password from the model dump
        password_hash=hashed_password)
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

@app.put("/customer/{customer_id}", response_model=Customer)
def update_customer(customer_id: int, customer: CustomerCreate, db: SessionDep):
    db_customer = db.query(CustomerDB).filter(CustomerDB.id == customer_id).first()
    print(customer_id, customer, db_customer)
    if not db_customer:
        return {"error": "Customer not found"}
    
    for key, value in customer.model_dump().items():
        setattr(db_customer, key, value)
    
    db.commit()
    db.refresh(db_customer)
    return db_customer

@app.patch("/customer/{customer_id}", response_model=Customer)
def patch_customer(customer_id: int, customer: CustomerPatch, db: SessionDep):
    db_customer = db.query(CustomerDB).filter(CustomerDB.id == customer_id).first()
    if not db_customer:
        return {"error": "Customer not found"}
    print(db_customer.email,db_customer.name,customer.model_dump(exclude_none=True))
    setattr(db_customer.email,db_customer.name, customer.model_dump(exclude_none=True).items())
    # for key, value in customer.model_dump().items():
    #     if value is not None:
    #         setattr(db_customer, key, value)
    db.commit()
    db.refresh(db_customer)
    return db_customer

@app.get("/customer/{customer_id}", response_model=Customer) #123
def get_customer(customer_id: int, password: str, db: SessionDep):
    customer = db.query(CustomerDB).filter(CustomerDB.id == customer_id).first()
    if not customer:
        return {"error": "Customer not found"}
    if verify_password(password, customer.password_hash):
        print("Password is correct")
    print(customer.password_hash)
    return customer

@app.get("/customers",response_model=list[Customer])
def list_customer(db: Session = Depends(get_database)):
    customers = db.query(CustomerDB).all()
    return customers
