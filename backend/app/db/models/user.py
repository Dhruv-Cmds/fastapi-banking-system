from sqlalchemy import String, Enum, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.core import UserRole, UserStatus
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from account import Account

from app.db import Base

class User (Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    username: Mapped[str] = mapped_column(
        String(100), 
        unique=True, 
        nullable=False,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(100), 
        nullable=False
    )

    password: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole),
        default=UserRole.USER,
        nullable=False ,
        index=True
    )

    status: Mapped[UserStatus] = mapped_column(
        Enum(UserStatus),
        default=UserStatus.ACTIVE,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.utcnow,
        nullable=False
    )

    accounts: Mapped["Account"] = relationship(
        "Account", 
        back_populates="owner"
    )