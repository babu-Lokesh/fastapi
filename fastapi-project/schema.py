from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class CustomerCreate(BaseModel):
    name: str
    email: str
    password: str

    

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