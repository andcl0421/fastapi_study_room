from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.repositories.reservation_repo import reservation_repo
from app.repositories.user_repo import user_repo
from app.repositories.room_repo import room_repo
from app.schemas.reservation import ReservationCreate, ReservationUpdate

class ReservationService:
    async def create_reservation_service(self, db: AsyncSession, data: ReservationCreate):
        user = await user_repo.get_user_by_id(db, data.user_id)
        if not user: raise HTTPException(status_code=404, detail="유저 없음")
        
        room = await room_repo.get_room_by_id(db, data.room_id)
        if not room: raise HTTPException(status_code=404, detail="방 없음")

        if data.user_count > room.max_capacity:
            raise HTTPException(status_code=400, detail="인원 초과")

        is_booked = await reservation_repo.check_overlap(
            db, data.room_id, data.reserve_date, data.start_time, data.end_time
        )
        if is_booked: raise HTTPException(status_code=400, detail="이미 예약됨")

        from app.models.reservation import Reservation
        new_res = Reservation(**data.model_dump(), status="CONFIRMED")
        return await reservation_repo.create_reservation(db, new_res)

    async def get_user_reservations(self, db: AsyncSession, user_id: int, status_filter: str = None):
        return await reservation_repo.get_reservations_by_user(db, user_id, status_filter)

    async def update_status_service(self, db: AsyncSession, reservation_id: int, data: ReservationUpdate):
        target = await reservation_repo.get_reservation_by_id(db, reservation_id) # 이름 맞춤
        if not target: raise HTTPException(status_code=404, detail="예약 없음")
        
        update_data = data.model_dump(exclude_unset=True)
        return await reservation_repo.update_reservation_fields(db, target, update_data)

    async def get_reservation_by_id(self, db: AsyncSession, reservation_id: int):
        res = await reservation_repo.get_reservation_by_id(db, reservation_id) # 이름 맞춤
        if not res: raise HTTPException(status_code=404, detail="예약 없음")
        return res

reservation_service = ReservationService()