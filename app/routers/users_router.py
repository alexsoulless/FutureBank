from fastapi import APIRouter, HTTPException, Query, Path, status, Depends, Body
from app.db import get_session
from sqlalchemy.future import select
from app.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exc, or_
from app.schemas.user import UserSchema, UserCreateSchema, UserUpdateSchema

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


@router.get("/find", response_model=list[UserSchema])
async def find_user(
    pattern: str = Query(min_length=3),
    session: AsyncSession = Depends(get_session),
):
    try:
        query = select(User).filter(
            or_(User.fio.like(f"%{pattern}%"), User.username.like(f"%{pattern}%"))
        )
        result = await session.execute(query)
        users = result.scalars().all()
        return users
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


@router.patch("/{user_id}", response_model=UserSchema)
async def update_user(
    user: UserUpdateSchema,
    user_id: int = Path(..., ge=1),
    session: AsyncSession = Depends(get_session),
):
    try:
        result = await session.execute(select(User).filter_by(id=user_id))
        db_user = result.scalar_one_or_none()
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")

        user_data = user.model_dump(exclude_unset=True)
        for key, value in user_data.items():
            setattr(db_user, key, value)

        await session.commit()
        await session.refresh(db_user)
        return UserSchema.model_validate(db_user)
    except exc.DatabaseError as ex:
        await session.rollback()
        orig = getattr(ex, "orig", None)
        detail = str(orig) if orig else str(ex)
        raise HTTPException(status_code=409, detail=detail)
    finally:
        await session.close()
