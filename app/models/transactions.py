from sqlalchemy import Column, Integer, ForeignKey, Numeric, DateTime, String
from datetime import datetime
from app.db import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    from_account_id = Column(Integer, ForeignKey("accounts.id"), nullable=True)
    to_account_id = Column(Integer, ForeignKey("accounts.id"), nullable=True)
    status = Column(String, default="ACTIVE")
    amount = Column(Numeric, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)