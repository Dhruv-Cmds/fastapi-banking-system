from sqlalchemy import Column, Integer, String
from db import engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Account (Base):

    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    acc_no = Column(String(10), unique=True, nullable=False)
    balance = Column(Integer)