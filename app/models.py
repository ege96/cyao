from passlib.context import CryptContext
from sqlalchemy import Column, Integer, String

from .database import Base

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=False, index=True)
    hashed_password = Column(String)

    def verify_password(self, plain_password):
        return pwd_context.verify(plain_password, self.hashed_password)
