from fastapi import Depends
from schema import CustomerDB
from passlib.context import CryptContext
from fastapi import APIRouter
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
import os
from db import session, sessionDep
auth_password_bearer = OAuth2PasswordBearer(tokenUrl="/token")
SECURITY_KEY = os.getenv("SECURITY_KEY")
ALGORITHM = os.getenv("ALGORITHM")

router = APIRouter(prefix="/token", tags=["Token"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_token(data: dict) -> str:
    return jwt.encode(data, SECURITY_KEY, algorithm=ALGORITHM)


def get_current_user(
    db: sessionDep, token: str = Depends(auth_password_bearer)
):
    try:
        print(f"Token: {token}")
        payload = jwt.decode(token, SECURITY_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        print(f"Email from token: {email}")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        customer = db.query(CustomerDB).filter(CustomerDB.email == email).first()
        if customer is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        print(f"Current User: {customer.name}")
        return customer
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/token")
def login(db: sessionDep, form_data: OAuth2PasswordRequestForm = Depends()):
    customer = db.query(CustomerDB).filter(CustomerDB.email == form_data.username).first()
    if not customer:
        return {"error": "Customer not found"}
    if verify_password(form_data.password, customer.password):
        token = create_token(data={"sub": customer.email})
        print(f"Generated Token: {token}")
        return {"access_token": token, "token_type": "bearer"}
    return {"error": "Invalid credentials"}
