from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.room import StudyRoom

class RoomRepository:
    # 1. 스터디룸 목록 가져오기 (필터링 기능 추가)
    async def get_all_rooms(
        self, 
        db: AsyncSession, 
        floor: int = None, 
        has_whiteboard: bool = None, 
        has_beam_projector: bool = None  # ◀ (수정) 인자 이름을 모델과 통일했습니다.
    ):
        """
        [심화 로직]
        사용자가 선택한 필터 조건이 있을 때만 쿼리에 추가합니다.
        """
        query = select(StudyRoom)
        
        # 층수 필터가 있으면 추가
        if floor is not None:
            query = query.where(StudyRoom.floor == floor)
            
        # 화이트보드 유무 필터
        if has_whiteboard is not None:
            query = query.where(StudyRoom.has_whiteboard == has_whiteboard)
            
        # 빔프로젝터 유무 필터
        if has_beam_projector is not None: # ◀ (수정) 변수명 통일
            query = query.where(StudyRoom.has_beam_projector == has_beam_projector)

        result = await db.execute(query)
        return result.scalars().all()

    # 2. 방 ID로 특정 방 하나 가져오기 (상세 조회용)
    async def get_room_by_id(self, db: AsyncSession, room_id: int):
        query = select(StudyRoom).where(StudyRoom.room_id == room_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    # 3. 방 이름으로 특정 방 하나 가져오기 (중복 체크용)
    async def get_room_by_name(self, db: AsyncSession, room_name: str):
        query = select(StudyRoom).where(StudyRoom.room_name == room_name)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    # 4. 새로운 스터디룸 데이터 저장하기 (방 생성용)
    async def create_room(self, db: AsyncSession, room_obj: StudyRoom):
        db.add(room_obj)
        await db.commit()
        await db.refresh(room_obj)
        return room_obj

    # 5. 스터디룸 정보 수정 (PATCH 반영)
    async def update_room(self, db: AsyncSession, db_room: StudyRoom, patch_data: dict):
        for key, value in patch_data.items():
            setattr(db_room, key, value)

        await db.commit()
        await db.refresh(db_room)
        return db_room

# 실물 객체 생성
room_repo = RoomRepository()