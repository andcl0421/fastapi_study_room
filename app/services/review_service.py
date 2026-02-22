from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.repositories.review_repo import review_repo
from app.repositories.reservation_repo import reservation_repo
from app.models.review import Review
from app.schemas.review import ReviewCreate

class ReviewService:
    async def create_review_service(self, db: AsyncSession, data: ReviewCreate, user_id: int):
        # 1. 해당 예약이 존재하는지 확인
        reservation = await reservation_repo.get_reservation_by_id(db, data.reservation_id)
        if not reservation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="리뷰를 작성할 예약 정보를 찾을 수 없습니다."
            )

        # 2. 본인의 예약이 맞는지 확인
        if reservation.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="본인의 예약에 대해서만 리뷰를 남길 수 있습니다."
            )

        # 3. 이미 이용이 완료된 예약인지 확인 (심화)
        if reservation.status != "COMPLETED":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="이용이 완료된 예약에 대해서만 리뷰를 남길 수 있습니다."
            )

        # 4. 리뷰 객체 생성 및 저장
        new_review = Review(
            reservation_id=data.reservation_id,
            user_id=user_id,
            room_id=reservation.room_id,
            content=data.content,
            rating=data.rating
        )
        
        return await review_repo.create_review(db, new_review)

    async def get_room_reviews(self, db: AsyncSession, room_id: int):
        return await review_repo.get_reviews_by_room(db, room_id)

review_service = ReviewService()