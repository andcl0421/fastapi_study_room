from datetime import datetime, time
from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import String, Integer, Text, Numeric, func, Boolean, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

# ❌ 수정 전: from app.models.user import Base
# ✅ 수정 후: 중앙 설계도 가방(database.py)에서 직접 가져옵니다.
from app.database import Base 

if TYPE_CHECKING:
    from app.models.reservation import Reservation

class StudyRoom(Base):
    """
    스터디룸의 물리적 정보와 운영 정보를 관리하는 테이블입니다.
    """
    __tablename__ = "study_rooms"

    # 1. 기본 식별 정보
    room_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    room_name: Mapped[str] = mapped_column(String(100), nullable=False)
    floor: Mapped[int] = mapped_column(Integer, nullable=False) 
    max_capacity: Mapped[int] = mapped_column(Integer, nullable=False) 
    description: Mapped[Optional[str]] = mapped_column(Text) 
    
    # 2. 시설물 정보 (UI 아이콘 표시용)
    has_whiteboard: Mapped[bool] = mapped_column(Boolean, server_default="0", nullable=False)
    has_beam_projector: Mapped[bool] = mapped_column(Boolean, server_default="0", nullable=False)
    
    # 3. 운영 시간 (예약 시간 검증 로직용)
    open_time: Mapped[time] = mapped_column(Time, server_default="09:00:00", nullable=False)
    close_time: Mapped[time] = mapped_column(Time, server_default="18:00:00", nullable=False)
    
    # 4. 이미지 및 평점
    room_image_url: Mapped[Optional[str]] = mapped_column(String(500))
    # asdecimal=False를 사용하여 파이썬에서 편리하게 float형으로 취급합니다.
    rating_avg: Mapped[float] = mapped_column(Numeric(2, 1, asdecimal=False), default=0.0) 
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    # 5. 관계 설정
    # 예약 테이블과 1:N 관계를 형성합니다.
    reservations: Mapped[List["Reservation"]] = relationship(back_populates="room")