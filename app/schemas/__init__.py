# app/schemas/__init__.py

from app.schemas.user import UserCreate, UserLogin, UserResponse, TokenResponse, UserUpdate
from app.schemas.room import RoomCreate, RoomUpdate, RoomResponse, RoomListResponse
from app.schemas.reservation import ReservationCreate, ReservationResponse
# from .token_schema import Token, TokenData   인증 관련 스키마가 있다면 없어서 미실행

# 외부에서 "from app.schemas import UserCreate"로 바로 쓸 수 있게 목록화
__all__ = [
    # User 관련
    "UserCreate", 
    "UserLogin", 
    "UserResponse", 
    "TokenResponse", 
    "UserUpdate",
    
    # Room 관련
    "RoomCreate", 
    "RoomUpdate", 
    "RoomResponse", 
    "RoomListResponse",
    
    # Reservation 관련
    "ReservationCreate", 
    "ReservationResponse"
]