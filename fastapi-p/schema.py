from pydantic import BaseModel, Field, EmailStr
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base



Base = declarative_base()

class CustomerDB(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, nullable=True)
    age = Column(Integer, nullable=False)
    password = Column(String)


class Customer(BaseModel):
    id:int = Field(..., ge=1, description="Customer ID must be a positive integer")
    name:str = Field(..., min_length=0, max_length=50)
    age:int = Field(..., ge=0, le=50, description="Customer's age must be between 0 and 50")
    email:EmailStr = Field(default=None, description="Customer's email address")
    password: str = Field(..., description="Hashed password of the customer")


class CustomerCreate(BaseModel):
    name:str = Field(..., min_length=3, max_length=50)
    age:int 
    email:EmailStr = Field(default=None, description="Customer's email address") 
    password: str    


class CustomerUpdate(BaseModel):
    name: str = Field(default=None, min_length=3, max_length=50)
    age: int = Field(default=None, ge=0, le=50, description="Customer's age must be between 0 and 50")
    email: EmailStr = Field(default=None, description="Customer's email address")
