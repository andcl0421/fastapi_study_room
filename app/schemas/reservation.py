from pydantic import BaseModel, ConfigDict, Field, model_validator
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

    # [실무 꿀팁] 시작 시간과 종료 시간의 선후 관계를 검증합니다. [cite: 2026-01-29]
    @model_validator(mode='after')
    def check_time_order(self):
        if self.start_time >= self.end_time:
            raise ValueError("종료 시간은 시작 시간보다 늦어야 합니다.") 
        return self

# 2. 상태 변경용 (수정)
class ReservationUpdate(BaseModel):
    status: Optional[str] = Field(None, pattern="^(CONFIRMED|CANCELLED|COMPLETED)$") # 상태 값 제한 [cite: 2026-01-28]
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












# from pydantic import BaseModel, ConfigDict, Field
# from datetime import datetime, date, time
# from typing import Optional

# # 1. 예약 신청용 (입력)
# class ReservationCreate(BaseModel):
#     user_id: int = Field(..., description="유저 고유 번호")
#     room_id: int = Field(..., description="방 번호")
#     reserve_date: date = Field(..., description="예약 날짜 (YYYY-MM-DD)")
#     start_time: time = Field(..., description="시작 시간 (HH:MM)")
#     end_time: time = Field(..., description="종료 시간 (HH:MM)")
#     user_count: int = Field(1, ge=1, description="이용 인원")

# # 2. 상태 변경용 (수정)
# class ReservationUpdate(BaseModel):
#     status: Optional[str] = None
#     admin_note: Optional[str] = None

# # 3. 예약 결과용 (출력)
# class ReservationResponse(BaseModel):
#     reservation_id: int
#     user_id: int
#     room_id: int
#     reserve_date: date
#     start_time: time
#     end_time: time
#     user_count: int
#     status: str
#     created_at: datetime

#     model_config = ConfigDict(from_attributes=True)