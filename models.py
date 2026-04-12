from sqlalchemy import Column, Integer, String, Float, ForeignKey
from db import engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Account (Base):

    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    acc_no = Column(String(10), unique=True, nullable=False)
    balance = Column(Float, default=0)
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="accounts")

class User (Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    password = Column(String(255), nullable=False)
    accounts = relationship("Account", back_populates="owner")