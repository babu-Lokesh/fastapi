import os

from fastapi import FastAPI
from schema import Base
from routes.customer import router as customer_router
from routes.token import router as token_router
from fastapi import FastAPI
from db import session,engine
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    Base.metadata.create_all(bind=engine)
    yield
    session.close()

app = FastAPI(lifespan=lifespan,
              title="Customer API", 
              description="API for managing customers", 
              version="1.0.0")

app.include_router(customer_router)
app.include_router(token_router)