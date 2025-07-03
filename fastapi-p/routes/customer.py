from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from schema import CustomerDB, Customer, CustomerCreate
from db import sessionDep
from .token import get_current_user, verify_password, get_password_hash

router = APIRouter(prefix="/customer", tags=["Customer"])

@router.get("/{customer_id}", response_model=Customer)
def get_customer(
    customer_id: int,
    password: str,
    db: sessionDep,
    current_user: CustomerDB = Depends(get_current_user)
):
    """
    Retrieve a customer by ID after verifying password.
    """
    customer = db.query(CustomerDB).filter(CustomerDB.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    if not verify_password(password, customer.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    return customer

@router.get("/", response_model=List[Customer])
def list_customers(
    db: sessionDep,
    current_user: CustomerDB = Depends(get_current_user)
):
    """
    List all customers.
    """
    return db.query(CustomerDB).all()

@router.post("/", response_model=Customer, status_code=status.HTTP_201_CREATED)
def create_customer(
    customer: CustomerCreate,
    db: sessionDep,
):
    """
    Create a new customer.
    """
    hashed_password = get_password_hash(customer.password)
    new_customer = CustomerDB(**customer.model_dump(exclude={"password"}), password=hashed_password)
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer

@router.put("/{customer_id}", response_model=Customer)
def update_customer(
    customer_id: int,
    customer_update: CustomerCreate,
    db: sessionDep,
    current_user: CustomerDB = Depends(get_current_user)
):
    """
    Update an existing customer.
    """
    customer = db.query(CustomerDB).filter(CustomerDB.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    for key, value in customer_update.model_dump(exclude_unset=True).items():
        if key == "password":
            value = get_password_hash(value)
        setattr(customer, key, value)
    db.commit()
    db.refresh(customer)
    return customer
