from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from ..repositories.room_repo import room_repo
from ..models.room import StudyRoom
from ..schemas.room import RoomCreate
from ..schemas.room import RoomUpdate # 새로 만든 수정 포장지 임포트
class RoomService:
    # 1. 모든 스터디룸 목록 가져오기
    async def get_rooms(self, db: AsyncSession):
        return await room_repo.get_all_rooms(db)

    # 2. 특정 스터디룸 상세 정보 가져오기
    async def get_room_by_id(self, db: AsyncSession, room_id: int):
        room = await room_repo.get_room_by_id(db, room_id)
        if not room:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="해당 스터디룸을 찾을 수 없습니다."
            )
        return room

    # 3. 새로운 스터디룸 등록
    async def create_room(self, db: AsyncSession, data: RoomCreate):
        existing_room = await room_repo.get_room_by_name(db, data.room_name)
        if existing_room:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="이미 존재하는 방 이름입니다."
            )

        new_room = StudyRoom(
            room_name=data.room_name,
            floor=data.floor,
            max_capacity=data.max_capacity,
            description=data.description
        )
        return await room_repo.create_room(db, new_room)

    # 4. 스터디룸 정보 수정 (PATCH)
    async def update_room_service(self, db: AsyncSession, room_id: int, data: RoomUpdate):
        # [STEP 1] 수정할 대상이 실제로 존재하는지 확인
        db_room = await room_repo.get_room_by_id(db, room_id)
        if not db_room:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="수정할 스터디룸이 존재하지 않습니다."
            )
    
        # [STEP 2] 클라이언트가 보낸 데이터 중 '값이 있는 것'만 딕셔너리로 변환
        # 예: 이름만 보냈으면 {'room_name': '새이름'} 만 남음
        patch_data = data.model_dump(exclude_unset=True) 
        
        # [STEP 3] 레포지토리에게 실제 수정을 맡김
        return await room_repo.update_room(db, db_room, patch_data)

# 실물 객체 생성
room_service = RoomService()