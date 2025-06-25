from fastapi import FastAPI,Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from schema import CustomerDB, Customer, CustomerCreate,Base
from typing import Annotated
from passlib.context import CryptContext

from fastapi import APIRouter

# database connection
DB_URL = "sqlite:///./my_sample.db"

engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

sessionDep = Annotated[session, Depends(get_db)]



app = FastAPI()
router = APIRouter(prefix="/customer", tags=["Customer"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# to get only one use
@router.get("/{customer_id}", response_model=Customer)
def customer(customer_id: int,password: str, db: sessionDep):
    customer = db.query(CustomerDB).filter(CustomerDB.id == customer_id).first()
    if not customer:
        return {"error": "Customer not found"}
    if verify_password(password, customer.password):
        print(f"Customer found: {customer.name}")
        return customer
    else:
        return {"error": "Invalid password"}


#list of customers
@router.get("/",response_model=list[Customer])
def list_customer(db: sessionDep):
    customers = db.query(CustomerDB).all()
    return customers

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# add new customer to my database
@router.post("/", response_model=Customer)
def customer(customer: CustomerCreate, db:sessionDep):
    pwd_hashed = get_password_hash(customer.password)
    print(f"Hashed Password: {pwd_hashed}")


    print(customer.model_dump())
    new_customer = CustomerDB(**customer.model_dump(exclude={"password"}), password=pwd_hashed)
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer
  
@router.put("/{customer_id}")
def customer(customer_id: int):
    pass

@router.patch("/{customer_id}")
def customer():
    pass


@router.delete("/{customer_id}")
def customer():
    pass

app.include_router(router)