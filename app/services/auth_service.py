import os
from dotenv import load_dotenv  # ★ 환경 변수 로드용
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from ..models.user import User
from ..repositories.user_repo import user_repo
from ..schemas.user import UserCreate, UserLogin

# .env 파일의 내용을 읽어옵니다. [cite: 2026-01-29]
load_dotenv()

# --- 환경 변수에서 설정값 불러오기 ---
# os.getenv는 .env 파일에 적힌 값을 가져옵니다. [cite: 2026-01-29]
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM")
# 분 단위는 숫자여야 하므로 int로 변환해줍니다. [cite: 2026-01-29]
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

# 1. 비밀번호 암호화 도구
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    # --- 비밀번호 처리 유틸리티 ---
    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    # --- 진짜 토큰(JWT) 생성기 ---
    def create_access_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        # 환경 변수에서 가져온 KEY와 ALGORITHM 사용 [cite: 2026-01-29]
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    # --- 회원가입 로직 ---
    async def signup(self, db: AsyncSession, data: UserCreate):
        existing_user = await user_repo.get_user_by_student_number(db, data.student_number)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="이미 등록된 학번입니다."
            )

        new_user = User(
            student_number=data.student_number,
            user_name=data.user_name,
            password=self.hash_password(data.password),
            user_role="user",
            penalty_count=0,
            is_active=True
        )
        return await user_repo.create_user(db, new_user)

    # --- 로그인 로직 ---
    async def login(self, db: AsyncSession, data: UserLogin):
        query = select(User).where(User.student_number == data.student_number)
        result = await db.execute(query)
        user = result.scalar_one_or_none()

        if not user or not self.verify_password(data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="학번 또는 비밀번호가 일치하지 않습니다."
            )

        # 환경 변수를 활용한 토큰 발행 [cite: 2026-01-29]
        access_token = self.create_access_token(data={"sub": str(user.user_id)})
        
        return {"access_token": access_token, "token_type": "bearer"}

auth_service = AuthService()