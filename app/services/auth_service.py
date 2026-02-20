from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status
from passlib.context import CryptContext
from ..models.user import User
from ..repositories.user_repo import user_repo
from ..schemas.user import UserCreate, UserLogin

# 1. 비밀번호 암호화 도구 (BCRYPT 알고리즘 사용)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    # --- 비밀번호 처리 유틸리티 ---
    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    # --- 회원가입 로직 ---
    async def signup(self, db: AsyncSession, data: UserCreate):
        # 직접 쿼리 짜지 말고 레포지토리에게 물어봅니다!
        existing_user = await user_repo.get_user_by_student_number(db, data.student_number)
        if existing_user:
            raise HTTPException(status_code=400, detail="이미 등록된 학번입니다.")

        new_user = User(
            student_number=data.student_number,
            user_name=data.user_name,
            password=self.hash_password(data.password)
        )
        
        # 저장도 레포지토리에게 시킵니다!
        return await user_repo.create_user(db, new_user)

        # 2. 비밀번호 암호화 및 유저 생성
        new_user = User(
            student_number=data.student_number,
            user_name=data.user_name,
            password=self.hash_password(data.password) # 암호화해서 저장!
        )
        
        db.add(new_user)
        await db.commit() # 실제 DB에 반영
        await db.refresh(new_user) # 생성된 ID 등을 다시 읽어옴
        return new_user

    # --- 로그인 로직 ---
    async def login(self, db: AsyncSession, data: UserLogin):
        # 1. 유저 찾기
        query = select(User).where(User.student_number == data.student_number)
        result = await db.execute(query)
        user = result.scalar_one_or_none()

        # 2. 유저가 없거나 비밀번호가 틀린 경우
        if not user or not self.verify_password(data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="학번 또는 비밀번호가 일치하지 않습니다."
            )

        # 3. 토큰 발급 (지금은 임시 문자열, 나중에 JWT 연동)
        return {"access_token": f"temp_token_for_{user.user_id}", "token_type": "bearer"}

# 실무 팁: 인스턴스를 미리 만들어두면 라우터에서 편하게 호출합니다.
auth_service = AuthService()