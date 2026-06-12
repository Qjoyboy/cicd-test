from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from internal.security.dependencies import get_current_user
from service.user_service import service_refresh_token, service_user_register, service_user_login
from internal.db.session import get_db
from schemas.user_schema import RefreshTokenRequest, UserCreate, UserLogin, UserRead

router = APIRouter(prefix="/user", tags=["user"])

DBConn = Annotated[AsyncSession, Depends(get_db)]

@router.post("/", response_model=UserRead, status_code=201)
async def register_user(session: DBConn, user: UserCreate):
    created_user = await service_user_register(session, user.email, user.username, user.password)
    return created_user


@router.post("/login")
async def login_user(session: DBConn, user: UserLogin):
    user = await service_user_login(session, user.email, user.password)
    return user


@router.post("/refresh")
async def refresh_token(data: RefreshTokenRequest):
    data = await service_refresh_token(data.refresh_token)
    return data


@router.get("/me")
async def me(
    current_user = Depends(get_current_user)
    ):
    return current_user