# 신규유저를 등록하거나 신분을 확인하고 열쇠(토큰)을 넘겨주는 로그인 역할

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession # AsyncSession 함수를 사용하기 위해서 async/await를 써야 매끄럽게 돌아감
from app.database import get_db
from app.services.auth_service import auth_service
from app.schemas.user import UserCreate, UserResponse, TokenResponse, UserLogin

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post(
    "/signup", 
    response_model=UserResponse, 
    status_code=status.HTTP_201_CREATED,
    summary="회원가입",
    description="새로운 사용자를 등록하고 정보를 반환합니다."
)
async def signup(data: UserCreate, db: AsyncSession = Depends(get_db)):
    # 💡 비동기 함수이므로 앞에 async를 붙이고, 내부에서 await를 사용
    return await auth_service.signup(db, data)

@router.post(
    "/login", 
    response_model=TokenResponse,
    summary="로그인",
    description="학번과 비밀번호로 로그인하여 토큰을 발급받습니다."
)
async def login(data: UserLogin, db: AsyncSession = Depends(get_db)):
    # 서비스 계층에서도 비동기 처리가 필요
    token_data = await auth_service.login(db, data)
    return token_data