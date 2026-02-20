from fastapi import FastAPI
from .database import engine  # 다시 점(.)을 붙여주세요
from .models import Base
from .routers import user as user
from .routers import rooms as rooms
from .routers import reservations as reservations
from app.routers.auth import router as auth_router
app = FastAPI(
    title="도봉캠퍼스 스터디룸 예약 시스템",
    description="실무형 비동기 DB 처리가 적용된 예약 API",
    version="1.1.0",
)

app.include_router(user.router)
app.include_router(rooms.router)
app.include_router(reservations.router)
app.include_router(auth_router)


# [STARTUP] 서버가 켜질 때 실행되는 로직
@app.on_event("startup")
async def init_tables():
    print("서버를 시작하며 DB 테이블을 생성합니다...")
    async with engine.begin() as conn:
        # 비동기 환경에서 테이블을 만드는 마법의 코드
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
async def read_root():
    return {"message": "스터디룸 예약 시스템이 정상 작동 중입니다!"}
