from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.database import get_db
from app.services.reservation_service import reservation_service
from app.schemas.reservation import ReservationCreate, ReservationResponse, ReservationUpdate

router = APIRouter(prefix="/reservations", tags=["Reservations"])

# 1. 예약하기
@router.post("/", response_model=ReservationResponse, status_code=status.HTTP_201_CREATED)
async def create_reservation(data: ReservationCreate, db: AsyncSession = Depends(get_db)):
    return await reservation_service.create_reservation_service(db, data)

# 2. 내 예약 목록 보기 (student_number 대신 user_id 사용 권장)
@router.get("/me", response_model=List[ReservationResponse])
async def get_my_reservations(
    user_id: int = Query(..., description="유저의 고유 ID"), 
    db: AsyncSession = Depends(get_db)
):
    return await reservation_service.get_user_reservations(db, user_id)

# 3. 예약 상태 수정 (취소 등)
@router.patch("/{reservation_id}/status", response_model=ReservationResponse)
async def update_reservation_status(
    reservation_id: int, 
    data: ReservationUpdate, 
    db: AsyncSession = Depends(get_db)
):
    return await reservation_service.update_status_service(db, reservation_id, data)