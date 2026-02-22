from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from ..repositories.room_repo import room_repo
from ..models.room import StudyRoom
from ..schemas.room import RoomCreate, RoomUpdate

class RoomService:
    # 1. 모든 스터디룸 목록 가져오기 (필터링 기능 추가)
    async def get_rooms(
        self, 
        db: AsyncSession, 
        floor: int = None, 
        has_whiteboard: bool = None, 
        has_projector: bool = None
    ):
        """
        [심화 로직] 
        단순 전체 조회가 아니라, 사용자가 선택한 조건(층수, 시설물)을 
        레포지토리에 전달하여 필터링된 결과를 가져옵니다.
        """
        return await room_repo.get_all_rooms(
            db, 
            floor=floor, 
            has_whiteboard=has_whiteboard, 
            has_projector=has_projector
        )

    # 2. 특정 스터디룸 상세 정보 가져오기
    async def get_room_by_id(self, db: AsyncSession, room_id: int):
        room = await room_repo.get_room_by_id(db, room_id)
        if not room:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="해당 스터디룸을 찾을 수 없습니다."
            )
        return room

    # 3. 새로운 스터디룸 등록 (시설물 및 운영 시간 추가)
    async def create_room(self, db: AsyncSession, data: RoomCreate):
        existing_room = await room_repo.get_room_by_name(db, data.room_name)
        if existing_room:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="이미 존재하는 방 이름입니다."
            )

        # [심화] 모델 확장에 맞춰 새 필드들을 포함하여 객체 생성
        new_room = StudyRoom(
            room_name=data.room_name,
            floor=data.floor,
            max_capacity=data.max_capacity,
            description=data.description,
            has_whiteboard=data.has_whiteboard, # 시설물 정보 추가
            has_beam_projector=data.has_beam_projector, # 시설물 정보 추가
            open_time=data.open_time, # 운영 시작 시간
            close_time=data.close_time, # 운영 종료 시간
            room_image_url=data.room_image_url # 이미지 경로
        )
        return await room_repo.create_room(db, new_room)

    # 4. 스터디룸 정보 수정 (PATCH)
    async def update_room_service(self, db: AsyncSession, room_id: int, data: RoomUpdate):
        db_room = await room_repo.get_room_by_id(db, room_id)
        if not db_room:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="수정할 스터디룸이 존재하지 않습니다."
            )
    
        # 클라이언트가 보낸 데이터 중 '값이 있는 것'만 딕셔너리로 변환
        patch_data = data.model_dump(exclude_unset=True) 
        
        return await room_repo.update_room(db, db_room, patch_data)

# 실물 객체 생성
room_service = RoomService()