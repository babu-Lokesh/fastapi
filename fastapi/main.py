from fastapi import FastAPI,Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from schema import CustomerDB, Customer, CustomerCreate,Base
from typing import Annotated

# database connection
DB_URL = "sqlite:///./my_sample.db"

engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine) # CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT, email TEXT UNIQUE, age INTEGER NOT NULL)

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

sessionDep = Annotated[session, Depends(get_db)]
app = FastAPI()

# to get only one use
@app.get("/customer/{customer_id}")
def customer(customer_id: int):
    pass

#list of customers
@app.get("/customer")
def customer_list():
    pass

# add new customer to my database
@app.post("/customer", response_model=Customer)
def customer(customer: CustomerCreate, db:sessionDep):

    print(customer.model_dump())
    new_customer = CustomerDB(**customer.model_dump())
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer
    # return {"message": "Customer added successfully", "customer": new_customer}
# git branch -M main
# git push -u origin main
# update customer in my database
@app.put("/customer/{customer_id}")
def customer(customer_id: int):
    pass

@app.patch("/customer/{customer_id}")
def customer():
    pass


@app.delete("/customer/{customer_id}")
def customer():
    pass