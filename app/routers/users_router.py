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