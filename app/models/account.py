from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base 


class Account (Base):

    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    acc_no = Column(Integer, unique=True, nullable=False)
    balance = Column(Numeric(10,2), default=0)
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="accounts")
    status = Column(String, default="ACTIVE")

