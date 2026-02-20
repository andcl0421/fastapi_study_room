from pydantic import BaseModel, ConfigDict, Field , EmailStr
from datetime import datetime
from typing import Optional

# 1. 회원가입할 때 유저가 보내는 데이터 (입력용)
class UserCreate(BaseModel):
    student_number: str = Field(..., min_length=5, max_length=20, description="학번")
    user_name: str = Field(..., min_length=2, max_length=50, description="이름")
    password: str = Field(..., min_length=4, description="비밀번호")

# 2. 로그인할 때 유저가 보내는 데이터 (입력용)
class UserLogin(BaseModel):
    student_number: str
    password: str

# 3. 유저 정보를 보여줄 때의 데이터 (출력용)
# 비밀번호 같은 민감한 정보는 빼고 보여줘야 함
class UserResponse(BaseModel):
    user_id: int
    student_number: str
    user_name: str
    created_at: datetime

    # SQLAlchemy 모델 객체를 Pydantic으로 변환하기 위한 설정
    model_config = ConfigDict(from_attributes=True)

# 4. 로그인 성공 시 발급하는 토큰 정보
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserUpdate(BaseModel):
    user_name: Optional[str] = None
    email: Optional[EmailStr] = None
    # 비밀번호는 보안상 보통 별도의 로직을 타거나, 필요할 때만 포함
    password: Optional[str] = None