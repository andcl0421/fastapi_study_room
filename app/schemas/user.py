from pydantic import BaseModel, ConfigDict, Field, EmailStr
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


# 3. 유저 정보를 보여줄 때의 데이터 (출력용) - 중복 제거 및 최적화
class UserResponse(BaseModel):
    user_id: int
    student_number: str
    user_name: str

    # [심화 추가] 기본값을 설정하여 500 에러 방지 (실무 표준)
    user_role: str = Field("user", description="사용자 권한 (user/admin)")
    penalty_count: int = Field(0, description="누적 패널티 횟수")
    is_active: bool = Field(True, description="계정 활성화 상태")

    created_at: datetime

    # DB 객체를 Pydantic 모델로 변환 가능하게 설정
    model_config = ConfigDict(from_attributes=True)


# 4. 유저 정보 수정 시 (입력용)
class UserUpdate(BaseModel):
    user_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

    # 관리자용 상태 변경 필드
    user_role: Optional[str] = None
    penalty_count: Optional[int] = None
    is_active: Optional[bool] = None


# 5. 로그인 성공 시 발급하는 토큰 정보
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
