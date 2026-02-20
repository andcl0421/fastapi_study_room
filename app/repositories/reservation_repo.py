from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from sqlalchemy.future import select
from sqlalchemy import and_
from app.models.reservation import Reservation
from app.schemas.reservation import ReservationCreate

class ReservationRepository:
    # 1. 예약 중복 확인 (실무 핵심 쿼리!)
    async def check_duplicate(self, db: AsyncSession, room_id: int, start: datetime, end: datetime):
        # 겹치는 조건: (기존 예약 시작 < 새 예약 종료) AND (기존 예약 종료 > 새 예약 시작)
        query = select(Reservation).where(
            and_(
                Reservation.room_id == room_id,
                Reservation.start_time < end,
                Reservation.end_time > start
            )
        )
        result = await db.execute(query)
        return result.scalar_one_or_none()

    # 2. 예약 저장
    async def create_reservation(self, db: AsyncSession, user_id: int, room_id: int, reserve_date, start_time, end_time):
            new_res = Reservation(
                user_id=user_id,
                room_id=room_id,
                reserve_date=reserve_date, # 추가
                start_time=start_time,
                end_time=end_time
            )
            db.add(new_res)
            await db.commit()
            await db.refresh(new_res)
            return new_res

    # 3. 유저 ID로 예약 목록 찾기
    async def get_by_user_id(self, db: AsyncSession, user_id: int):
        query = select(Reservation).where(Reservation.user_id == user_id)
        result = await db.execute(query)
        return result.scalars().all()

    # 4. 예약 ID로 하나 찾기
    async def get_by_id(self, db: AsyncSession, res_id: int):
        query = select(Reservation).where(Reservation.reservation_id == res_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    # 5. 예약 삭제 (취소)
    async def delete_reservation(self, db: AsyncSession, reservation: Reservation):
        await db.delete(reservation)
        await db.commit()
        return {"message": "정상적으로 취소되었습니다."}

reservation_repo = ReservationRepository()