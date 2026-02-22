from fastapi import FastAPI
from .database import engine
from .models import Base

# ★ 중요: 테이블을 만들기 위해 모든 모델을 여기서 임포트해야 합니다.
# 이렇게 해야 Base.metadata에 "아, 이런 테이블을 만들어야지!" 하고 정보가 등록됩니다.
from app.models.user import User
from app.models.room import StudyRoom
from app.models.reservation import Reservation
from app.models.review import Review

# 라우터 임포트 (이름 중복 방지를 위해 명확하게 별칭 지정)
from .routers import user as user_mod
from .routers import rooms as rooms_mod
from .routers import reservations as res_mod
from app.routers.auth import router as auth_router
from app.routers.reviews import router as review_router

app = FastAPI(
    title="도봉캠퍼스 스터디룸 예약 시스템",
    description="실무형 비동기 DB 처리가 적용된 예약 API",
    version="1.1.0",
)

# 라우터 등록
app.include_router(user_mod.router)
app.include_router(rooms_mod.router)
app.include_router(res_mod.router)
app.include_router(auth_router)
app.include_router(review_router)

# [STARTUP] 서버가 켜질 때 실행되는 로직
@app.on_event("startup")
async def init_tables():
    print("--------------------------------------------------")
    print("서버를 시작하며 DB 테이블을 생성합니다...")
    async with engine.begin() as conn:
        # 이제 상단에서 모델들을 임포트했기 때문에 Base가 모든 테이블 정보를 인지합니다.
        await conn.run_sync(Base.metadata.create_all)
    print("DB 테이블 생성 완료!")
    print("--------------------------------------------------")

@app.get("/")
async def read_root():
    return {"message": "스터디룸 예약 시스템이 정상 작동 중입니다!"}

# from fastapi import FastAPI
# # 1. database.py에서 engine과 '진짜' Base를 가져옵니다.
# from app.database import engine, Base 

# # 2. 테이블 생성을 위해 모든 모델 클래스를 임포트합니다. (이 과정은 아주 잘하셨어요!)
# from app.models.user import User
# from app.models.room import StudyRoom
# from app.models.reservation import Reservation
# from app.models.review import Review

# # 3. 라우터 임포트
# from app.routers import user, rooms, reservations, auth, reviews

# app = FastAPI(
#     title="도봉캠퍼스 스터디룸 예약 시스템",
#     version="1.1.0",
# )

# # 라우터 등록
# app.include_router(auth.router)
# app.include_router(user.router)
# app.include_router(rooms.router)
# app.include_router(reservations.router)
# app.include_router(reviews.router)

# @app.on_event("startup")
# async def init_tables():
#     print("--------------------------------------------------")
#     print("🚀 [시스템] DB 테이블 생성을 시작합니다...")
#     try:
#         async with engine.begin() as conn:
#             # 중앙 Base.metadata를 사용해 연결된 모든 모델(User, Room 등)을 생성합니다.
#             await conn.run_sync(Base.metadata.create_all)
#         print("✅ [시스템] 모든 DB 테이블이 성공적으로 생성되었습니다!")
#     except Exception as e:
#         print(f"❌ [에러] 테이블 생성 중 문제가 발생했습니다: {e}")
#     print("--------------------------------------------------")

# @app.get("/")
# async def read_root():
#     return {"message": "정상 작동 중입니다!"}