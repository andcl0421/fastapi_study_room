from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

# [1] 생성용 (아까 만든 것)
class RoomCreate(BaseModel):
    room_name: str = Field(..., min_length=1, max_length=100)
    floor: int = Field(..., ge=1)
    max_capacity: int = Field(..., gt=0)
    description: Optional[str] = None

# [2] 수정용 (Update) - ★ 실무 필수!
# 모든 필드를 'Optional'로 만들어서, 바꾸고 싶은 것만 보낼 수 있게 함
class RoomUpdate(BaseModel):
    room_name: Optional[str] = None
    floor: Optional[int] = None
    max_capacity: Optional[int] = None
    description: Optional[str] = None

# [3] 응답용 (Response) - 상세 정보용
class RoomResponse(BaseModel):
    room_id: int
    room_name: str
    floor: int
    max_capacity: int
    description: Optional[str]
    rating_avg: float

    model_config = ConfigDict(from_attributes=True)

# [4] 목록용 (Simple Response) - ★ 데이터 절약용!
# 방 리스트를 보여줄 땐 굳이 긴 설명(description)이 필요 없음
class RoomListResponse(BaseModel):
    room_id: int
    room_name: str
    max_capacity: int
    rating_avg: float

    model_config = ConfigDict(from_attributes=True)