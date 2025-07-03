from fastapi import APIRouter, Depends, Response, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated
import uuid
from ..schema import CustomerCreate, Customer, CustomerPatch
from ..models import CustomerDB
from ..database import SessionDep, get_database
from ..authentication import get_current_user, get_password_hash, verify_password, create_access_token
from ..constants import session_store

token_router = APIRouter(prefix="/token",tags=["token"])

@token_router.post("/login")
def login(
    db: SessionDep ,
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    
):
    user = db.query(CustomerDB).filter(CustomerDB.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    # JWT token
    access_token = create_access_token(data={"sub": user.email})
    # Session cookie
    
    session_id = str(uuid.uuid4())
    #session_store[session_id] = user.email
    session_store.set(f"session:{session_id}", user.email)
    
    print(session_store) #Redis or any other storage can be used here
    response.set_cookie(
        key="session_id",
        value=session_id, #47cd039a-94c3-42a4-9920-84b64887ad5c - 7ecd8023-e602-4394-8eee-68f0d1de88d8
        httponly=True,
        max_age=60*60*24,
        samesite="lax",
        secure=False  # Set to True in production
    )
    return {"access_token": access_token, "token_type": "bearer", "session_id": session_id}


@token_router.post("/logout")
def logout(response: Response, request: Request):
    session_id = request.cookies.get("session_id")
    if session_id:
        session_store.delete(f"session:{session_id}")
        #session_store.pop(session_id, None)
    response.delete_cookie("session_id")
    return {"message": "Logged out"}