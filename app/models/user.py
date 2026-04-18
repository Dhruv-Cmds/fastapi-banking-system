from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db import Base

class User (Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    password = Column(String(255), nullable=False)
    accounts = relationship("Account", back_populates="owner")