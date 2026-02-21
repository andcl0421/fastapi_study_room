from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database import get_db
from app.services.room_service import room_service
from app.schemas.room import RoomResponse, RoomCreate
from app.schemas.room import RoomUpdate

router = APIRouter(prefix="/rooms", tags=["Rooms"])


# 1. 모든 스터디룸 목록 조회
@router.get("/", response_model=List[RoomResponse], summary="전체 스터디룸 목록 조회")
async def get_all_rooms(db: AsyncSession = Depends(get_db)):
    # 서비스에게 모든 방을 가져오라고 시킴
    return await room_service.get_rooms(db)


# 2. 특정 스터디룸 상세 조회
@router.get(
    "/{room_id}", response_model=RoomResponse, summary="특정 스터디룸 상세 정보"
)
async def get_room_detail(room_id: int, db: AsyncSession = Depends(get_db)):
    return await room_service.get_room_by_id(db, room_id)


# 3. 새로운 스터디룸 등록 (관리자용)
@router.post(
    "/",
    response_model=RoomResponse,
    status_code=status.HTTP_201_CREATED,
    summary="새로운 스터디룸 등록",
)
async def create_new_room(data: RoomCreate, db: AsyncSession = Depends(get_db)):
    return await room_service.create_room(db, data)


@router.patch("/{room_id}", response_model=RoomResponse)
async def update_room(
    room_id: int, data: RoomUpdate, db: AsyncSession = Depends(get_db)
):
    return await room_service.update_room_service(db, room_id, data)
