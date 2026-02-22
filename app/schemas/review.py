from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional

# 리뷰 작성용
class ReviewCreate(BaseModel):
    reservation_id: int = Field(..., description="어떤 예약에 대한 리뷰인지")
    content: str = Field(..., min_length=5, description="리뷰 내용 (최소 5자)")
    rating: int = Field(..., ge=1, le=5, description="별점 (1~5점)")

# 리뷰 응답용
class ReviewResponse(BaseModel):
    review_id: int
    reservation_id: int
    user_id: int
    room_id: int
    content: str
    rating: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)