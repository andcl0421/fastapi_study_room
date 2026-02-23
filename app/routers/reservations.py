
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database import get_db
from app.services.reservation_service import reservation_service
from app.schemas.reservation import ReservationCreate, ReservationResponse, ReservationUpdate

router = APIRouter(prefix="/reservations", tags=["Reservations"])

# 1. 예약하기 (비즈니스 로직: 과거 날짜 금지, 2시간 제한 포함)
@router.post(
    "/", 
    response_model=ReservationResponse, 
    status_code=status.HTTP_201_CREATED,
    summary="새로운 예약 생성",
    description="과거 날짜 예약 불가, 인당 하루 최대 2시간 제한 로직이 서비스 계층에서 검증됩니다."
)
async def create_reservation(
    data: ReservationCreate, 
    db: AsyncSession = Depends(get_db)
):
    """
    [비즈니스 로직 흐름]
    1. 서비스 계층에서 '과거 날짜'인지 확인 [cite: 2026-01-29]
    2. 서비스 계층에서 '하루 2시간 이용 제한' 확인 [cite: 2026-01-29]
    3. 중복 예약 여부 확인 후 저장 [cite: 2026-01-29]
    """
    return await reservation_service.create_reservation_service(db, data)

# 2. 내 예약 목록 보기
@router.get("/me", response_model=List[ReservationResponse])
async def get_my_reservations(
    user_id: int = Query(..., description="조회할 유저의 고유 ID"), 
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


# from fastapi import APIRouter, Depends, HTTPException, status, Query
# from sqlalchemy.ext.asyncio import AsyncSession
# from typing import List, Optional

# from app.database import get_db
# from app.services.reservation_service import reservation_service
# from app.schemas.reservation import ReservationCreate, ReservationResponse, ReservationUpdate

# router = APIRouter(prefix="/reservations", tags=["Reservations"])

# # 1. 예약하기
# @router.post("/", response_model=ReservationResponse, status_code=status.HTTP_201_CREATED)
# async def create_reservation(data: ReservationCreate, db: AsyncSession = Depends(get_db)):
#     return await reservation_service.create_reservation_service(db, data)

# # 2. 내 예약 목록 보기 (student_number 대신 user_id 사용 권장)
# @router.get("/me", response_model=List[ReservationResponse])
# async def get_my_reservations(
#     user_id: int = Query(..., description="유저의 고유 ID"), 
#     db: AsyncSession = Depends(get_db)
# ):
#     return await reservation_service.get_user_reservations(db, user_id)

# # 3. 예약 상태 수정 (취소 등)
# @router.patch("/{reservation_id}/status", response_model=ReservationResponse)
# async def update_reservation_status(
#     reservation_id: int, 
#     data: ReservationUpdate, 
#     db: AsyncSession = Depends(get_db)
# ):
#     return await reservation_service.update_status_service(db, reservation_id, data)