from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.repositories.user_repo import user_repo
from app.schemas.user import UserResponse

class UserService:
    # 1. 내 정보 상세 조회
    async def get_user_info(self, db: AsyncSession, student_number: str):
        user = await user_repo.get_user_by_student_number(db, student_number)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="존재하지 않는 사용자입니다."
            )
        return user

    # 2. 회원 탈퇴
    async def withdraw_user(self, db: AsyncSession, user_id: int):
        # 여기에 나중에 user_repo.delete_user(db, user_id)를 만들어서 연결할 거예요!
        pass

# 라우터에서 사용할 실물 객체 생성
user_service = UserService()