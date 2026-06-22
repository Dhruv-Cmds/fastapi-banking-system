from sqlalchemy import Column, Enum, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from datetime import datetime

from app.core import UserStatus
from app.db import Base

class Transaction(Base):

    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)

    from_account_id: Mapped[int] = mapped_column(
        ForeignKey("accounts.id"), 
        nullable=True,
        index=True
    )

    to_account_id: Mapped[int] = mapped_column(
        ForeignKey("accounts.id"), 
        nullable=True,
        index=True
    )

    status: Mapped[UserStatus] = mapped_column(
        Enum(UserStatus), 
        default=UserStatus.ACTIVE,
        nullable=False,
    )

    amount = Column(Numeric, nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.utcnow,
        nullable=False
    )