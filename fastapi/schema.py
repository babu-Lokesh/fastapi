from pydantic import BaseModel, Field, EmailStr

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

#SQLModel


Base = declarative_base()

class CustomerDB(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, nullable=True)
    age = Column(Integer, nullable=False)





class Customer(BaseModel):
    id:int = Field(..., ge=1, description="Customer ID must be a positive integer")
    name:str = Field(..., min_length=3, max_length=50)
    age:int = Field(..., ge=0, le=50, description="Customer's age must be between 0 and 50")
    email:EmailStr = Field(default=None, description="Customer's email address")

class CustomerCreate(BaseModel):
    name:str 
    age:int 
    email:EmailStr = Field(default=None, description="Customer's email address")    