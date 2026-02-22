from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import time


# [1] 생성용 (RoomCreate)
class RoomCreate(BaseModel):
    room_name: str = Field(..., min_length=1, max_length=100)
    floor: int = Field(..., ge=1)
    max_capacity: int = Field(..., gt=0)
    description: Optional[str] = None

    # [심화 추가] 시설물 및 운영 정보
    has_whiteboard: bool = False
    has_beam_projector: bool = False
    open_time: time = time(9, 0)  # 기본값 09:00
    close_time: time = time(18, 0)  # 기본값 18:00
    room_image_url: Optional[str] = None


# [2] 수정용 (RoomUpdate)
class RoomUpdate(BaseModel):
    room_name: Optional[str] = None
    floor: Optional[int] = None
    max_capacity: Optional[int] = None
    description: Optional[str] = None

    # [심화 추가] 수정 가능한 필드 확장
    has_whiteboard: Optional[bool] = None
    has_beam_projector: Optional[bool] = None
    open_time: Optional[time] = None
    close_time: Optional[time] = None
    room_image_url: Optional[str] = None


# [3] 응답용 (RoomResponse) - 상세 정보용
class RoomResponse(BaseModel):
    room_id: int
    room_name: str
    floor: int
    max_capacity: int
    description: Optional[str]

    # [심화 추가] 출력 필드 확장
    has_whiteboard: bool
    has_beam_projector: bool
    open_time: time
    close_time: time
    room_image_url: Optional[str] = None

    rating_avg: float

    model_config = ConfigDict(from_attributes=True)


# [4] 목록용 (RoomListResponse) - 리스트 조회용
class RoomListResponse(BaseModel):
    room_id: int
    room_name: str
    floor: int
    max_capacity: int
    has_whiteboard: bool
    has_beam_projector: bool
    room_image_url: Optional[str] = None
    rating_avg: float

    model_config = ConfigDict(from_attributes=True)
