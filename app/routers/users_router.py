from fastapi import APIRouter, HTTPException, Query, Path, status, Depends
from app.db import get_session
from sqlalchemy.future import select
from app.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserSchema

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[UserSchema])
async def get_users(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User))
    users = result.scalars().all()
    return users


@router.get("/{user_id}", response_model=UserSchema)
async def get_user(
    session: AsyncSession = Depends(get_session), user_id: int = Path(..., ge=1)
):
    result = await session.execute(select(User).filter_by(id=user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserSchema(**user)
