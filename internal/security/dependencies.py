from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from internal.security.jwt import decode_token
from internal.db.session import get_db
from repo.user_repo import get_user_by_id
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/user/login"
)

async def get_current_user(
        token: str = Depends(oauth2_scheme), 
        session: AsyncSession = Depends(get_db)
        ):
    payload = decode_token(token)

    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Invalod token"
        )
    user_id = payload.get("sub")

    user = await get_user_by_id(session, int(user_id))
    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )
    return user