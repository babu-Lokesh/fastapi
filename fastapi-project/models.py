
# database

# two tabels Customer and Order

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base 
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List

Base = declarative_base()

class CustomerDB(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)

    orders = relationship("OrderDB", back_populates="customer")


class OrderDB(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    product:str = Field(..., max_length=100)
    quantity = Column(Integer,)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    customer = relationship("CustomerDB", back_populates="orders")
    
#MVC

class CustomerCreate(BaseModel):
    name: str
    email: str

    

class OrderCreate(BaseModel):
    product: str
    quantity: int
    customer_id: int

class CustomerPatch(BaseModel):
    name: Optional[str] = Field (None, max_length=100)
    email: Optional[EmailStr] = Field (None, max_length=100)

   

class Customer(BaseModel):
    id: int
    name: str
    email: str
 
    class Config:
        orm_mode = True  
           
class Order(BaseModel):
    id: int
    product: str
    quantity: int
    customer_id: int

    class Config:
        orm_mode = True