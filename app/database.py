import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase  # ★ 핵심: 설계도 가방을 만드는 도구입니다.

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# 1. DB 엔진 생성 (통로)
engine = create_async_engine(DATABASE_URL, echo=True)

# 2. 세션 공장 (세션을 찍어내는 도구)
# 실무에서는 이름을 조금 더 명확하게 'factory'라고 붙이기도 합니다.
async_session_factory = async_sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

# 3. ★ 이 부분이 빠졌습니다! (설계도 보관함)
# 이 Base를 User, Room 모델에서 가져가서 상속받아야 합니다.
class Base(DeclarativeBase):
    pass

# 4. FastAPI의 의존성 주입(Depends)용 함수
async def get_db():
    # 위에서 만든 공장(factory)을 사용합니다.
    async with async_session_factory() as session:
        try:
            yield session
        finally:
            # 작업이 끝나면 안전하게 연결을 닫습니다.
            await session.close()