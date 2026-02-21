from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User

class UserRepository:
    # 1. 학번으로 유저 찾기 (로그인, 내 정보 조회용)
    async def get_user_by_student_number(self, db: AsyncSession, student_number: str):
        # 💡 [심화] 탈퇴하지 않은(is_active=True) 유저만 찾는 로직을 기본으로 할 수도 있습니다.
        query = select(User).where(User.student_number == student_number)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    # 2. [추가] 고유 ID(PK)로 유저 찾기
    async def get_user_by_id(self, db: AsyncSession, user_id: int):
        """
        서비스 계층에서 패널티 부여나 탈퇴 처리를 할 때 
        정확히 한 명을 집어내기 위해 반드시 필요합니다.
        """
        query = select(User).where(User.user_id == user_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    # 3. 새로운 유저 저장하기 (회원가입)
    async def create_user(self, db: AsyncSession, user_obj: User):
        db.add(user_obj)
        await db.commit()
        await db.refresh(user_obj)
        return user_obj

    # 4. [추가] 유저 정보 업데이트 (패널티, 상태 변경 등)
    async def update_user(self, db: AsyncSession, user_obj: User):
        """
        변경된 penalty_count나 is_active 상태를 DB에 최종 저장합니다.
        """
        await db.commit()
        await db.refresh(user_obj)
        return user_obj

# 실물 객체 생성
user_repo = UserRepository()