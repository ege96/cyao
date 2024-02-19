import os
from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException, Depends
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from ..database import SessionLocal
from ..dependencies import authenticate_user, get_current_user
from ..schemas import UserLogin

router = APIRouter()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")  # Defaulting to HS256 if not specified
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))  # Defaulting to 30 minutes

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=30)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def refresh_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if "exp" in payload and datetime.fromtimestamp(payload["exp"]) < datetime.utcnow():
            del payload["exp"]
            return create_access_token(data=payload)
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")


@router.post("/token/")
async def login_for_access_token(user_login: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, user_login.email, user_login.password)
    if user is None:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/token/refresh/")
async def refresh_access_token_route(data: dict = Depends(get_current_user)):
    return {"access_token": refresh_access_token(data["token"]), "token_type": "bearer"}
