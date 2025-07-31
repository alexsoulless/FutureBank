from fastapi import APIRouter, HTTPException, Query, Path, status, Depends, Body
from app.db import get_session
from sqlalchemy.future import select
from app.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exc
from app.schemas.user import UserSchema, UserCreateSchema

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[UserSchema])
async def get_users(session: AsyncSession = Depends(get_session)):
    try:
        result = await session.execute(select(User))
        users = result.scalars().all()
        return users
    except Exception as ex:
        raise ex
    finally:
        await session.close()


@router.get("/{user_id}", response_model=UserSchema)
async def get_user(
    session: AsyncSession = Depends(get_session), user_id: int = Path(..., ge=1)
):
    try:
        result = await session.execute(select(User).filter_by(id=user_id))
        user = result.scalar_one_or_none()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return UserSchema(**user)
    finally:
        await session.close()

@router.post("", response_model=UserSchema)
async def create_user(
    user: UserCreateSchema,
    session: AsyncSession = Depends(get_session),
):
    try:
        new_user = User(**user.model_dump())
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return UserSchema.model_validate(new_user)
    except exc.DatabaseError as ex:
        await session.rollback()
        orig = getattr(ex, "orig", None)
        detail = str(orig) if orig else str(ex)
        raise HTTPException(status_code=409, detail=detail)
    finally:
        await session.close()