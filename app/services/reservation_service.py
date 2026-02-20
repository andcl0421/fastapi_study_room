from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from datetime import datetime

from ..repositories.reservation_repo import reservation_repo
from ..repositories.user_repo import user_repo
from ..repositories.room_repo import room_repo
from ..schemas.reservation import ReservationCreate

class ReservationService:
    # 1. 예약 생성 (가장 중요한 로직!)
    async def create_reservation_service(self, db: AsyncSession, data: ReservationCreate):
        # [검증 1] 존재하는 유저인지 확인
        user = await user_repo.get_user_by_student_number(db, data.student_number)
        if not user:
            raise HTTPException(status_code=404, detail="존재하지 않는 학생입니다.")

        # [검증 2] 존재하는 방인지 확인
        room = await room_repo.get_room_by_id(db, data.room_id)
        if not room:
            raise HTTPException(status_code=404, detail="존재하지 않는 스터디룸입니다.")

        # [검증 3] ★ 실무 핵심: 중복 예약 확인 (같은 시간대에 이미 예약이 있는지)
        # 이 로직은 나중에 레포지토리에 get_overlap_reservation 함수를 만들어서 체크할 거예요.
        is_booked = await reservation_repo.check_duplicate(db, data.room_id, data.start_time, data.end_time)
        if is_booked:
            raise HTTPException(status_code=400, detail="해당 시간대에는 이미 예약이 꽉 찼습니다.")

        # [저장] 모든 검증을 통과하면 예약 저장!
        return await reservation_repo.create_reservation(
                db, 
                user_id=user.user_id,
                room_id=data.room_id,
                reserve_date=data.start_time.date(),  # 날짜 추출
                start_time=data.start_time.time(),    # 시작 시간 추출
                end_time=data.end_time.time()        # 종료 시간 추출
            )
    # 2. 내 예약 목록 조회
    async def get_user_reservations(self, db: AsyncSession, student_number: str):
        user = await user_repo.get_user_by_student_number(db, student_number)
        if not user:
            raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
        
        return await reservation_repo.get_by_user_id(db, user.user_id)

    # 3. 예약 취소
    async def cancel_reservation_service(self, db: AsyncSession, reservation_id: int):
        target = await reservation_repo.get_by_id(db, reservation_id)
        if not target:
            raise HTTPException(status_code=404, detail="취소할 예약 내역이 없습니다.")
            
        return await reservation_repo.delete_reservation(db, target)

reservation_service = ReservationService()