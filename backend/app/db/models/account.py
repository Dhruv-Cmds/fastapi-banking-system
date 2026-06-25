from sqlalchemy import Column, Enum, Numeric, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.core import AccountStatus

from app.db import Base 

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from user import User

class Account (Base):

    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True)

    acc_no: Mapped[int] = mapped_column(
        unique=True, 
        nullable=False,
        index=True
    )
    
    balance = Column(Numeric(10,2), default=0)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    status: Mapped[AccountStatus] = mapped_column(
        Enum(AccountStatus),
        default=AccountStatus.ACTIVE,
        nullable=False,
        index=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.utcnow,
        nullable=False
    )

    # RELATIONSHIPS

    owner: Mapped["User"] = relationship(
        "User", 
        back_populates="accounts"
    )

