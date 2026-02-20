from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime, date, time
from typing import Optional

# 1. 예약 신청용 포장지 (Input)
# 손님이 "어떤 방을, 언제부터, 언제까지" 빌릴지 적는 양식입니다.
class ReservationCreate(BaseModel):
    student_number: str = Field(..., description="예약자 학번")
    room_id: int = Field(..., description="예약할 방 번호")
    start_time: datetime = Field(..., description="예약 시작 시간 (예: 2026-02-20T14:00:00)")
    end_time: datetime = Field(..., description="예약 종료 시간 (예: 2026-02-20T16:00:00)")

# 2. 예약 결과 보여주기용 포장지 (Output)
# 예약이 완료된 후 영수증처럼 보여주는 정보입니다.
class ReservationResponse(BaseModel):
    reservation_id: int
    user_id: int
    room_id: int
    reserve_date: date        # 추가: 날짜 칸
    start_time: time         # 수정: datetime -> time
    end_time: time           # 수정: datetime -> time
    status: str              # 추가: 예약 상태
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)