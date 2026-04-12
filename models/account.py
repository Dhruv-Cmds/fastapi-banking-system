from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base 


class Account (Base):

    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    acc_no = Column(String(10), unique=True, nullable=False)
    balance = Column(Float, default=0)
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="accounts")

