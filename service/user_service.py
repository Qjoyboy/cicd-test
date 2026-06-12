from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from internal.security.jwt import create_access_token, create_refresh_token, decode_token
from internal.security.security import hash_password, verify_password
from repo.user_repo import get_user_by_email, repo_create_user

async def service_user_register(
        session: AsyncSession, 
        email: str, 
        username: str, 
        password: str
        ):
    exist_user = await get_user_by_email(session, email)
    if exist_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    hashed_password = hash_password(password)

    user = await repo_create_user(session, email, username, hashed_password)
    return user

async def service_user_login(session: AsyncSession, email: str, password: str):
    exist_user = await get_user_by_email(session, email)
    if not exist_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not verify_password(password, exist_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(exist_user.id)
    refresh_token = create_refresh_token(exist_user.id)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type":"bearer"
    }

async def service_refresh_token(refresh_token: str):
    payload = decode_token(refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(int(user_id))

    return {
        "access_token":access_token,
        "token_type":"bearer"
    }