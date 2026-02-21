from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database import get_db
from app.services.reservation_service import reservation_service
from app.schemas.reservation import ReservationCreate, ReservationResponse

router = APIRouter(prefix="/reservations", tags=["Reservations"])

# 1. 예약하기 (Create)
@router.post("/", response_model=ReservationResponse, status_code=status.HTTP_201_CREATED, summary="스터디룸 예약")
async def create_reservation(data: ReservationCreate, db: AsyncSession = Depends(get_db)):
    # "사장님, 여기 예약 하나 추가요!"
    return await reservation_service.create_reservation_service(db, data)

# 2. 내 예약 목록 보기 (Read - List)
@router.get("/me", response_model=List[ReservationResponse], summary="내 예약 내역 조회")
async def get_my_reservations(student_number: str, db: AsyncSession = Depends(get_db)):
    # "내가 빌린 방들이 뭐가 있지?"
    return await reservation_service.get_user_reservations(db, student_number)

# 3. 예약 취소하기 (Delete)
@router.delete("/{reservation_id}", summary="예약 취소")
async def cancel_reservation(reservation_id: int, db: AsyncSession = Depends(get_db)):
    # "앗, 일정이 생겨서 취소할게요"
    return await reservation_service.cancel_reservation_service(db, reservation_id)