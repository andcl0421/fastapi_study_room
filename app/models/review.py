from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Text, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .user import Base

if TYPE_CHECKING:
    from .reservation import Reservation
    from .user import User

class Review(Base):
    __tablename__ = "reviews"

    review_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    reservation_id: Mapped[int] = mapped_column(ForeignKey("reservations.reservation_id", ondelete="CASCADE"), unique=True, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    room_id: Mapped[int] = mapped_column(ForeignKey("study_rooms.room_id", ondelete="CASCADE"), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    reservation: Mapped["Reservation"] = relationship(back_populates="review")
    user: Mapped["User"] = relationship(back_populates="reviews")