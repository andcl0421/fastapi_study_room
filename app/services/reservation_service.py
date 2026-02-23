from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from datetime import datetime, date
import logging # 에러 추적을 위한 로그 추가

from app.repositories.reservation_repo import reservation_repo
from app.repositories.user_repo import user_repo
from app.repositories.room_repo import room_repo
from app.schemas.reservation import ReservationCreate, ReservationUpdate

# 로그 설정 (실무에서 에러 파악용)
logger = logging.getLogger(__name__)

class ReservationService:
    async def create_reservation_service(self, db: AsyncSession, data: ReservationCreate):
        # [1] 기본 정보 확인
        user = await user_repo.get_user_by_id(db, data.user_id)
        if not user: 
            raise HTTPException(status_code=404, detail="존재하지 않는 유저입니다.")
        
        room = await room_repo.get_room_by_id(db, data.room_id)
        if not room: 
            raise HTTPException(status_code=404, detail="존재하지 않는 스터디룸입니다.")

        # [2] 비즈니스 로직: 과거 날짜 예약 불가
        if data.reserve_date < date.today():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="과거 날짜로는 예약할 수 없습니다."
            )

        # [3] 비즈니스 로직: 인원 초과 확인
        if data.user_count > room.max_capacity:
            raise HTTPException(
                status_code=400, 
                detail=f"최대 수용 인원({room.max_capacity}명)을 초과했습니다."
            )

        # [4] 비즈니스 로직: 하루 2시간(120분) 이용 제한
        today_reservations = await reservation_repo.get_reservations_by_user(db, data.user_id)
        total_minutes = 0
        
        for res in today_reservations:
            if res.status != "CANCELLED" and res.reserve_date == data.reserve_date:
                start_dt = datetime.combine(res.reserve_date, res.start_time)
                end_dt = datetime.combine(res.reserve_date, res.end_time)
                total_minutes += (end_dt - start_dt).seconds // 60

        current_duration = (datetime.combine(data.reserve_date, data.end_time) - 
                          datetime.combine(data.reserve_date, data.start_time)).seconds // 60
        
        if (total_minutes + current_duration) > 120:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=f"하루 최대 이용 시간(120분)을 초과했습니다. (현재 이용: {total_minutes}분)"
            )

        # [5] 중복 예약 확인
        is_booked = await reservation_repo.check_overlap(
            db, data.room_id, data.reserve_date, data.start_time, data.end_time
        )
        if is_booked: 
            raise HTTPException(status_code=400, detail="해당 시간대에 이미 예약이 존재합니다.")

        # [6] 저장
        from app.models.reservation import Reservation
        new_res = Reservation(**data.model_dump(), status="CONFIRMED")
        return await reservation_repo.create_reservation(db, new_res)

    async def get_user_reservations(self, db: AsyncSession, user_id: int, status_filter: str = None):
        return await reservation_repo.get_reservations_by_user(db, user_id, status_filter)

    async def update_status_service(self, db: AsyncSession, reservation_id: int, data: ReservationUpdate):
        target = await reservation_repo.get_reservation_by_id(db, reservation_id)
        if not target: raise HTTPException(status_code=404, detail="예약 내역을 찾을 수 없습니다.")
        
        update_data = data.model_dump(exclude_unset=True)
        return await reservation_repo.update_reservation_fields(db, target, update_data)

    async def get_reservation_by_id(self, db: AsyncSession, reservation_id: int):
        res = await reservation_repo.get_reservation_by_id(db, reservation_id)
        if not res: raise HTTPException(status_code=404, detail="예약 내역을 찾을 수 없습니다.")
        return res


reservation_service = ReservationService()




















# from sqlalchemy.ext.asyncio import AsyncSession
# from fastapi import HTTPException, status
# from app.repositories.reservation_repo import reservation_repo
# from app.repositories.user_repo import user_repo
# from app.repositories.room_repo import room_repo
# from app.schemas.reservation import ReservationCreate, ReservationUpdate

# class ReservationService:
#     async def create_reservation_service(self, db: AsyncSession, data: ReservationCreate):
#         user = await user_repo.get_user_by_id(db, data.user_id)
#         if not user: raise HTTPException(status_code=404, detail="유저 없음")
        
#         room = await room_repo.get_room_by_id(db, data.room_id)
#         if not room: raise HTTPException(status_code=404, detail="방 없음")

#         if data.user_count > room.max_capacity:
#             raise HTTPException(status_code=400, detail="인원 초과")

#         is_booked = await reservation_repo.check_overlap(
#             db, data.room_id, data.reserve_date, data.start_time, data.end_time
#         )
#         if is_booked: raise HTTPException(status_code=400, detail="이미 예약됨")

#         from app.models.reservation import Reservation
#         new_res = Reservation(**data.model_dump(), status="CONFIRMED")
#         return await reservation_repo.create_reservation(db, new_res)

#     async def get_user_reservations(self, db: AsyncSession, user_id: int, status_filter: str = None):
#         return await reservation_repo.get_reservations_by_user(db, user_id, status_filter)

#     async def update_status_service(self, db: AsyncSession, reservation_id: int, data: ReservationUpdate):
#         target = await reservation_repo.get_reservation_by_id(db, reservation_id) # 이름 맞춤
#         if not target: raise HTTPException(status_code=404, detail="예약 없음")
        
#         update_data = data.model_dump(exclude_unset=True)
#         return await reservation_repo.update_reservation_fields(db, target, update_data)

#     async def get_reservation_by_id(self, db: AsyncSession, reservation_id: int):
#         res = await reservation_repo.get_reservation_by_id(db, reservation_id) # 이름 맞춤
#         if not res: raise HTTPException(status_code=404, detail="예약 없음")
#         return res

# reservation_service = ReservationService()