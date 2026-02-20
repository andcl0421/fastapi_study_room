from datetime import datetime
from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import String, Integer, Text, Numeric, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.user import Base  # user.py에서 Base를 가져옴

if TYPE_CHECKING:
    from app.models.reservation import Reservation

class StudyRoom(Base):
    __tablename__ = "study_rooms"

    room_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    room_name: Mapped[str] = mapped_column(String(100), nullable=False)
    floor: Mapped[int] = mapped_column(Integer, nullable=False)
    max_capacity: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    rating_avg: Mapped[float] = mapped_column(Numeric(2, 1, asdecimal=False),  default=0.0) #asdecimal=False 단순 숫자로 편하게 쓰기위해 옵션추가
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    reservations: Mapped[List["Reservation"]] = relationship(back_populates="room")

    