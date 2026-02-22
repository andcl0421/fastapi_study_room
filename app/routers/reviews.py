from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db
from app.schemas.review import ReviewCreate, ReviewResponse
# 서비스 레이어는 생략하고 레포지토리로 바로 연결하는 예시입니다.
from app.repositories.review_repo import review_repo
from app.models.review import Review

router = APIRouter(prefix="/reviews", tags=["Reviews"])

@router.post("/", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
async def create_review(data: ReviewCreate, db: AsyncSession = Depends(get_db)):
    # 실무팁: 원래는 Service에서 예약 정보(reservation_id)를 확인하는 로직이 들어가야 함
    new_review = Review(
        reservation_id=data.reservation_id,
        content=data.content,
        rating=data.rating,
        user_id=1, # 임시: 나중엔 로그인 정보에서 가져옴
        room_id=1  # 임시: 예약 정보에서 가져옴
    )
    return await review_repo.create_review(db, new_review)