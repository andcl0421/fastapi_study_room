from datetime import datetime, date, time
from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, ForeignKey, Date, Time, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .user import Base

if TYPE_CHECKING:
    from .user import User
    from .study_room import StudyRoom
    from .review import Review

class Reservation(Base):
    __tablename__ = "reservations"

    reservation_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    room_id: Mapped[int] = mapped_column(ForeignKey("study_rooms.room_id", ondelete="CASCADE"), nullable=False)
    reserve_date: Mapped[date] = mapped_column(Date, nullable=False)
    start_time: Mapped[time] = mapped_column(Time, nullable=False)
    end_time: Mapped[time] = mapped_column(Time, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="CONFIRMED")
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    user: Mapped["User"] = relationship(back_populates="reservations")
    room: Mapped["StudyRoom"] = relationship(back_populates="reservations")
    review: Mapped[Optional["Review"]] = relationship(back_populates="reservation", uselist=False)