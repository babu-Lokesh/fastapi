from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Annotated
from ..schema import CustomerCreate, Customer, CustomerPatch
from ..models import CustomerDB
from ..database import SessionDep, get_database
from ..authentication import get_current_user, get_password_hash

router_customer = APIRouter(prefix="/customer", tags=["api"])

@router_customer.post("/customer", response_model=Customer)
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
Current_user_DP = Annotated[CustomerDB, Depends(get_current_user)]

@router_customer.put("/customer/{customer_id}", response_model=Customer, )
def update_customer(customer_id: int, customer: CustomerCreate, db: SessionDep, current_user: CustomerDB = Depends(get_current_user)):
    db_customer = db.query(CustomerDB).filter(CustomerDB.id == customer_id).first()
    print(customer_id, customer, db_customer)
    if not db_customer:
        return {"error": "Customer not found"}
    
    for key, value in customer.model_dump().items():
        setattr(db_customer, key, value)
    
    db.commit()
    db.refresh(db_customer)
    return db_customer

@router_customer.patch("/customer/{customer_id}", response_model=Customer)
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

@router_customer.get("/customer/{customer_id}", response_model=Customer) #123
def get_customer(customer_id: int, db: SessionDep,current_user: CustomerDB = Depends(get_current_user)):
    customer = db.query(CustomerDB).filter(CustomerDB.id == customer_id).first()
    if not customer:
        return {"error": "Customer not found"}
    
    print(customer.password_hash)
    return customer



@router_customer.get("/customers",response_model=list[Customer])
def list_customer(db:SessionDep, current_user: CustomerDB = Depends(get_current_user)):
    customers = db.query(CustomerDB).all()
    return customers