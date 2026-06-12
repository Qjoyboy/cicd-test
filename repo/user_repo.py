from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from internal.models.user_model import User


async def repo_create_user(
        session: AsyncSession, 
        email: str, 
        username: str, 
        hashed_password: str
        ):
    user = User(email=email, username=username, hashed_password=hashed_password)
    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user

async def get_user_by_email(        
        session: AsyncSession, 
        email: str, 
        ):
    result = await session.execute(
        select(User).where(User.email == email)
    )

    return result.scalar_one_or_none()

async def get_user_by_id(        
        session: AsyncSession, 
        user_id: int, 
        ):
    result = await session.execute(
        select(User).where(User.id == user_id)
    )

    return result.scalar_one_or_none()
