from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database import get_db
from app.repositories.user_repo import user_repo
from app.schemas.user import UserResponse  # 💡 Schema 파일도 나중에 수정해야 합니다!

router = APIRouter(prefix="/users", tags=["Users"])

# 1. 내 정보 조회 (학번 기반)
@router.get("/me", response_model=UserResponse, summary="내 정보 상세 조회")
async def get_my_info(student_number: str, db: AsyncSession = Depends(get_db)):
    """
    [심화 로직] 
    단순 조회를 넘어, 해당 유저의 penalty_count와 user_role을 함께 반환합니다.
    """
    user = await user_repo.get_user_by_student_number(db, student_number)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="해당 학번의 사용자를 찾을 수 없습니다."
        )
    
    # [심화] 계정이 비활성화 상태인지 확인하는 로직 추가
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="비활성화된 계정입니다. 관리자에게 문의하세요."
        )
        
    return user

# 2. 유저 상태 업데이트 (예: 패널티 부여 또는 권한 변경)
# 이 기능은 보통 '관리자'만 사용할 수 있도록 나중에 보안 처리를 추가합니다.
@router.patch("/{user_id}/status", summary="유저 상태 및 패널티 수정")
async def update_user_status(
    user_id: int, 
    penalty_score: int = 0, 
    db: AsyncSession = Depends(get_db)
):
    """
    [심화 로직]
    노쇼 발생 시 관리자가 유저의 패널티 점수를 올리는 용도로 사용합니다.
    """
    # 실제 구현 시 user_repo.update_penalty 등을 호출
    return {"message": f"유저 {user_id}의 패널티가 {penalty_score}점으로 업데이트되었습니다."}

# 3. 회원 탈퇴 (소프트 삭제 권장)
@router.delete("/{user_id}", summary="회원 탈퇴 처리")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    """
    실무에서는 데이터를 완전히 지우기보다 'is_active = False'로 바꾸는 
    소프트 삭제(Soft Delete)를 많이 사용합니다.
    """
    return {"message": f"유저 {user_id} 계정이 비활성화(탈퇴) 처리되었습니다."}