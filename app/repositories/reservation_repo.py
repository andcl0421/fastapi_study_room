from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_
from app.models.reservation import Reservation

class ReservationRepository:
    async def check_overlap(self, db: AsyncSession, room_id: int, reserve_date, start_time, end_time):
        query = select(Reservation).where(
            and_(
                Reservation.room_id == room_id,
                Reservation.reserve_date == reserve_date,
                Reservation.status != "CANCELLED",
                Reservation.start_time < end_time,
                Reservation.end_time > start_time
            )
        )
        result = await db.execute(query)
        return result.scalars().first()

    async def create_reservation(self, db: AsyncSession, res_obj: Reservation):
        db.add(res_obj)
        await db.commit()
        await db.refresh(res_obj)
        return res_obj

    async def get_reservations_by_user(self, db: AsyncSession, user_id: int, status_filter: str = None):
        query = select(Reservation).where(Reservation.user_id == user_id)
        if status_filter: query = query.where(Reservation.status == status_filter)
        result = await db.execute(query.order_by(Reservation.reserve_date.desc()))
        return result.scalars().all()

    async def get_reservation_by_id(self, db: AsyncSession, reservation_id: int):
        query = select(Reservation).where(Reservation.reservation_id == reservation_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def update_reservation_fields(self, db: AsyncSession, db_res: Reservation, patch_data: dict):
        for key, value in patch_data.items():
            setattr(db_res, key, value)
        await db.commit()
        await db.refresh(db_res)
        return db_res

reservation_repo = ReservationRepository()