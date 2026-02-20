from datetime import datetime
from typing import List, TYPE_CHECKING
from sqlalchemy import String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

# 여기서 Base를 선언합니다. 다른 파일들은 'from .user import Base'로 가져가면 됩니다.
class Base(DeclarativeBase):
    pass

if TYPE_CHECKING:
    from app.models.reservation import Reservation
    from app.models.review import Review

class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    student_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    user_name: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    reservations: Mapped[List["Reservation"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    reviews: Mapped[List["Review"]] = relationship(back_populates="user")