from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User

class UserRepository:
    # 1. 학번으로 유저 찾기 (로그인, 중복 검사 때 사용)
    async def get_user_by_student_number(self, db: AsyncSession, student_number: str):
        query = select(User).where(User.student_number == student_number)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    # 2. 새로운 유저 저장하기 (회원가입 때 사용)
    async def create_user(self, db: AsyncSession, user_obj: User):
        db.add(user_obj)
        await db.commit()
        await db.refresh(user_obj)
        return user_obj

# 실무 팁: 서비스와 마찬가지로 인스턴스를 미리 만들어둡니다.
user_repo = UserRepository()