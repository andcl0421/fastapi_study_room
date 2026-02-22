from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.review import Review

class ReviewRepository:
    async def create_review(self, db: AsyncSession, review_obj: Review):
        db.add(review_obj)
        await db.commit()
        await db.refresh(review_obj)
        return review_obj

    async def get_reviews_by_room(self, db: AsyncSession, room_id: int):
        query = select(Review).where(Review.room_id == room_id)
        result = await db.execute(query)
        return result.scalars().all()

review_repo = ReviewRepository()