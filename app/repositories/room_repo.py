from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.room import StudyRoom

class RoomRepository:
    # 1. 모든 스터디룸 가져오기 (목록 조회용)
    async def get_all_rooms(self, db: AsyncSession):
        query = select(StudyRoom)
        result = await db.execute(query)
        return result.scalars().all() # 여러 명의 데이터를 리스트로 가져옴

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
        await db.commit()      # DB에 확정 저장
        await db.refresh(room_obj) # 자동 생성된 ID 등을 다시 읽어오기
        return room_obj
    

    async def update_room(self, db: AsyncSession, db_room: StudyRoom, patch_data: dict):
    # 딕셔너리에 담긴 내용대로 DB 객체의 값을 하나씩 갈아끼웁니다.
        for key, value in patch_data.items():
            setattr(db_room, key, value)

        await db.commit()      # DB에 확정 저장 (Commit)
        await db.refresh(db_room) # 최신 정보로 새로고침
        return db_room

# 라우터나 서비스에서 임포트할 실물 객체
room_repo = RoomRepository()