from datetime import datetime
from typing import List, TYPE_CHECKING
from sqlalchemy import String, func, Integer, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

# 공통 Base 클래스
class Base(DeclarativeBase):
    pass

if TYPE_CHECKING:
    from app.models.reservation import Reservation
    from app.models.review import Review

class User(Base):
    __tablename__ = "users"

    # 기본 정보
    user_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    student_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    user_name: Mapped[str] = mapped_column(String(50), nullable=False)
    
    # [심화 추가] 권한 및 상태 관리
    # role: 'user' 또는 'admin' 저장. 기본값은 'user'
    user_role: Mapped[str] = mapped_column(String(20), server_default="user", nullable=False)
    
    # [심화 추가] 서비스 규칙 (패널티 시스템)
    # penalty_count: 노쇼 발생 시 1씩 증가. 실무에선 이 숫자로 예약 가능 여부를 판단합니다.
    penalty_count: Mapped[int] = mapped_column(Integer, server_default="0", nullable=False)
    
    # [심화 추가] 계정 활성화 여부
    is_active: Mapped[bool] = mapped_column(Boolean, server_default="1", nullable=False)

    # 타임스탬프
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    # 관계 설정 (기존 유지)
    reservations: Mapped[List["Reservation"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    reviews: Mapped[List["Review"]] = relationship(back_populates="user")