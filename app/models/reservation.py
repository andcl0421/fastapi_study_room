from datetime import datetime, date, time
from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, ForeignKey, Date, Time, func, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

# ❌ 수정 전: from app.models.user import Base
# ✅ 수정 후: 중앙 설계도 가방(database.py)에서 직접 가져옵니다.
from app.database import Base 

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.room import StudyRoom
    from app.models.review import Review

class Reservation(Base):
    """
    유저가 특정 스터디룸을 언제, 얼마나 이용할지 기록하는 핵심 테이블입니다.
    """
    __tablename__ = "reservations"

    # 1. 고유 식별자 및 연결 고리(FK)
    reservation_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False
    )
    room_id: Mapped[int] = mapped_column(
        ForeignKey("study_rooms.room_id", ondelete="CASCADE"), nullable=False
    )
    
    # 2. 예약 상세 일정
    reserve_date: Mapped[date] = mapped_column(Date, nullable=False)
    start_time: Mapped[time] = mapped_column(Time, nullable=False)
    end_time: Mapped[time] = mapped_column(Time, nullable=False)
    
    # 3. 비즈니스 로직 필드
    # user_count: 실제 몇 명이 오는지 체크 (룸 수용 인원과 비교 시 사용)
    user_count: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    
    # status: 예약의 현재 상태 (실무 표준 상태 관리)
    status: Mapped[str] = mapped_column(String(20), server_default="CONFIRMED", nullable=False)
    
    # admin_note: 관리자가 특이사항을 메모하는 용도
    admin_note: Mapped[Optional[str]] = mapped_column(Text)
    
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    # 4. 객체 간 관계 설정 (ORM 지름길)
    user: Mapped["User"] = relationship(back_populates="reservations")
    room: Mapped["StudyRoom"] = relationship(back_populates="reservations")
    
    # review: 예약 하나당 리뷰 하나만 (1:1 관계)
    review: Mapped[Optional["Review"]] = relationship(
        "Review", back_populates="reservation", uselist=False
    )
