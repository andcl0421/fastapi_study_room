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
            
        # [심화] 정지된 유저인지 확인
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="패널티 누적 또는 탈퇴로 인해 이용이 제한된 계정입니다."
            )
            
        return user

    # 2. 패널티 부여 및 자동 정지 로직
    async def apply_penalty(self, db: AsyncSession, user_id: int):
        """
        노쇼가 발생했을 때 호출됩니다. 
        패널티가 3점이 되면 계정을 자동으로 비활성화합니다.
        """
        user = await user_repo.get_user_by_id(db, user_id) # 리포지토리에 ID 조회 기능 필요
        if not user:
            raise HTTPException(status_code=404, detail="유저를 찾을 수 없습니다.")

        user.penalty_count += 1
        
        # 실무 규칙: 패널티 3회 이상 시 자동 정지
        if user.penalty_count >= 3:
            user.is_active = False
            
        await db.commit()
        return user

    # 3. 회원 탈퇴 (Soft Delete)
    async def withdraw_user(self, db: AsyncSession, user_id: int):
        """
        [실무형] 데이터를 지우지 않고 'is_active' 상태만 변경합니다.
        이래야 나중에 이 유저가 예약했던 내역(통계)을 확인할 수 있어요!
        """
        user = await user_repo.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="유저를 찾을 수 없습니다.")
            
        user.is_active = False
        await db.commit()
        return {"message": "정상적으로 탈퇴 처리되었습니다."}

# 라우터에서 사용할 실물 객체 생성
user_service = UserService()