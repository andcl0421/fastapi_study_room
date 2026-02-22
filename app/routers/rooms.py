from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.database import get_db
from app.services.room_service import room_service
from app.schemas.room import RoomResponse, RoomCreate, RoomUpdate

router = APIRouter(prefix="/rooms", tags=["Rooms"])

# 1. 스터디룸 목록 조회 (필터링 기능 추가)
@router.get("/", response_model=List[RoomResponse], summary="스터디룸 목록 조회 및 필터링")
async def get_all_rooms(
    floor: Optional[int] = Query(None, description="층별 필터 (예: 4, 5)"),
    has_whiteboard: Optional[bool] = Query(None, description="화이트보드 유무"),
    has_projector: Optional[bool] = Query(None, description="빔프로젝터 유무"),
    db: AsyncSession = Depends(get_db)
):
    """
    [심화 로직]
    - 사진 속 층별 탭(전체/4층/5층) 클릭 시 floor 값을 넘겨받아 필터링합니다.
    - 시설물 아이콘 필터 선택 시 해당 시설이 있는 방만 골라냅니다.
    """
    return await room_service.get_rooms(db, floor=floor, has_whiteboard=has_whiteboard, has_projector=has_projector)

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
    # 나중에 유저 권한(admin) 확인 로직을 여기에 추가할 수 있습니다.
    return await room_service.create_room(db, data)

# 4. 스터디룸 정보 수정
@router.patch("/{room_id}", response_model=RoomResponse, summary="스터디룸 정보 수정")
async def update_room(
    room_id: int, data: RoomUpdate, db: AsyncSession = Depends(get_db)
):
    return await room_service.update_room_service(db, room_id, data)
