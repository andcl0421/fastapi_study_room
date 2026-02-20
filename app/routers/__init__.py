from app.routers.user import router as user_router
from app.routers.rooms import router as room_router
from app.routers.reservations import router as reservation_router
from app.routers.auth import router as auth_router

# 이렇게 해두면 main.py에서 'from .routers import user_router'로 바로 쓸 수 있음

__all__ = [
    "user_router",
    "room_router",
    "reservation_router",
    "auth_router"
]