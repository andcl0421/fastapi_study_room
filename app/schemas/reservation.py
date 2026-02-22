from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime, date, time
from typing import Optional

# 1. 예약 신청용 (입력)
class ReservationCreate(BaseModel):
    user_id: int = Field(..., description="유저 고유 번호")
    room_id: int = Field(..., description="방 번호")
    reserve_date: date = Field(..., description="예약 날짜 (YYYY-MM-DD)")
    start_time: time = Field(..., description="시작 시간 (HH:MM)")
    end_time: time = Field(..., description="종료 시간 (HH:MM)")
    user_count: int = Field(1, ge=1, description="이용 인원")

# 2. 상태 변경용 (수정)
class ReservationUpdate(BaseModel):
    status: Optional[str] = None
    admin_note: Optional[str] = None

# 3. 예약 결과용 (출력)
class ReservationResponse(BaseModel):
    reservation_id: int
    user_id: int
    room_id: int
    reserve_date: date
    start_time: time
    end_time: time
    user_count: int
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)