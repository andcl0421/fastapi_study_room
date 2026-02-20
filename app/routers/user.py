from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database import get_db
from app.repositories.user_repo import user_repo
from app.schemas.user import UserResponse

router = APIRouter(prefix="/users", tags=["Users"])

# 1. 내 정보 조회 (지금은 간단히 학번으로 조회하는 예시)
@router.get("/me", response_model=UserResponse, summary="내 정보 조회")
async def get_my_info(student_number: str, db: AsyncSession = Depends(get_db)):
    user = await user_repo.get_user_by_student_number(db, student_number)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="사용자를 찾을 수 없습니다."
        )
    return user

# 2. 특정 유저 삭제 (회원 탈퇴 등)
@router.delete("/{user_id}", summary="회원 탈퇴")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    # 나중에 레포지토리에 delete_user 기능을 추가해서 연결하면 됨
    return {"message": f"유저 {user_id} 삭제 완료 (기능 구현 중)"}