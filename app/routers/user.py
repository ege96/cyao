from fastapi import APIRouter, Depends, HTTPException
from passlib.context import CryptContext  # Importing Passlib for password hashing
from sqlalchemy.orm import Session

from .. import crud, schemas, dependencies

router = APIRouter()

# Creating a PassLib Context for hashing passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/users/", response_model=schemas.UserInDB)
def create_user(user: schemas.UserCreate, db: Session = Depends(dependencies.get_db)):
    db_user = crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    # Hashing the password before storing it in the database
    hashed_password = pwd_context.hash(user.password)
    return crud.create_user(db=db,
                            user=schemas.UserCreate(email=user.email,
                                                    password=hashed_password))


@router.delete("/users/{user_id}", response_model=schemas.UserDelete)
def delete_user(user_id: int, db: Session = Depends(dependencies.get_db)):
    return crud.delete_user(db, user_id)


@router.put("/users/{user_id}", response_model=schemas.UserUpdate)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(dependencies.get_db)):
    user.password = pwd_context.hash(user.password)
    return crud.update_user(db, user_id, user)
