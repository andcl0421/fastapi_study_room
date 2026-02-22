from datetime import datetime
from typing import List, TYPE_CHECKING
from sqlalchemy import String, func, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

# ★ 중요: database.py에서 만든 공통 설계도(Base)를 가져옵니다.
# 이렇게 해야 main.py에서 이 모델을 인식하고 테이블을 만들어줍니다.
from app.database import Base

if TYPE_CHECKING:
    from app.models.reservation import Reservation
    from app.models.review import Review

class User(Base):
    """
    유저 정보를 담는 테이블 모델입니다.
    """
    __tablename__ = "users"

    # 1. 기본 식별 정보
    # 실무 팁: id는 명확하게 user_id로 명명하여 관계 설정 시 헷갈리지 않게 합니다.
    user_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    student_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    user_name: Mapped[str] = mapped_column(String(50), nullable=False)
    
    # 2. 권한 및 상태 관리 (비즈니스 로직)
    # user_role: 관리자(admin)와 일반유저(user) 구분
    user_role: Mapped[str] = mapped_column(String(20), server_default="user", nullable=False)
    
    # penalty_count: 노쇼(No-Show) 횟수 기록 (실무형 패널티 시스템)
    penalty_count: Mapped[int] = mapped_column(Integer, server_default="0", nullable=False)
    
    # is_active: 계정 사용 가능 여부 (삭제 대신 비활성화를 주로 사용함)
    is_active: Mapped[bool] = mapped_column(Boolean, server_default="1", nullable=False)

    # 3. 자동 타임스탬프
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    # 4. 연관 관계 설정
    # cascade="all, delete-orphan": 유저 삭제 시 관련 예약도 함께 정리합니다.
    reservations: Mapped[List["Reservation"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    reviews: Mapped[List["Review"]] = relationship(back_populates="user")