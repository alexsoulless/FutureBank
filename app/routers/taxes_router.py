from fastapi import APIRouter, HTTPException, Query, Path, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import exc
from app.schemas.tax import TaxSchema, TaxCreateSchema, TaxUpdateSchema
from app.schemas.tax_payment import TaxStatsSchema
from app.schemas.user import UserSchema 
from app.models import Tax, User, TaxPayment
from app.db import get_session

router = APIRouter(prefix="/taxes", tags=["taxes"])


@router.post("", response_model=TaxSchema)
async def create_tax(tax: TaxCreateSchema, session: AsyncSession = Depends(get_session)):
    try:
        new_tax = Tax(**tax.model_dump())
        session.add(new_tax)
        await session.commit()
        await session.refresh(new_tax)
        return new_tax
    finally:
        await session.close()


@router.get("", response_model=list[TaxSchema])
async def get_taxes(session: AsyncSession = Depends(get_session)):
    try:
        result = await session.execute(select(Tax))
        taxes = result.scalars().all()
        return taxes
    finally:
        await session.close()


@router.get("/{tax_id}", response_model=TaxSchema)
async def get_tax(
    tax_id: int = Path(ge=1), session: AsyncSession = Depends(get_session)
):
    try:
        result = await session.execute(select(Tax).filter_by(id=tax_id))
        tax = result.scalar_one_or_none()
        if tax is None:
            raise HTTPException(status_code=404, detail="Tax not found")
        return tax
    finally:
        await session.close()


@router.patch("/{tax_id}", response_model=TaxSchema)
async def update_tax(
    tax: TaxUpdateSchema,
    tax_id: int = Path(..., ge=1),
    session: AsyncSession = Depends(get_session),
):
    try:
        result = await session.execute(select(Tax).filter_by(id=tax_id))
        db_tax = result.scalar_one_or_none()
        if db_tax is None:
            raise HTTPException(status_code=404, detail="Tax not found")

        tax_data = tax.model_dump(exclude_unset=True)
        for key, value in tax_data.items():
            setattr(db_tax, key, value)

        await session.commit()
        await session.refresh(db_tax)
        return db_tax
    except exc.DatabaseError as ex:
        await session.rollback()
        orig = getattr(ex, "orig", None)
        detail = str(orig) if orig else str(ex)
        raise HTTPException(status_code=409, detail=detail)
    finally:
        await session.close()


@router.get("/{tax_id}/stats", response_model=TaxStatsSchema)
async def get_tax_stats(
    tax_id: int = Path(..., ge=1),
    session: AsyncSession = Depends(get_session),
):
    try:
        result = await session.execute(select(Tax).filter_by(id=tax_id))
        db_tax = result.scalar_one_or_none()
        if db_tax is None:
            raise HTTPException(status_code=404, detail="Tax not found")

        payed_result = await session.execute(
            select(User).join(TaxPayment).filter(TaxPayment.tax_id == tax_id)
        )
        payed_users = payed_result.scalars().all()

        not_payed_result = await session.execute(
            select(User).where(
                ~User.id.in_(
                    select(TaxPayment.user_id).filter(TaxPayment.tax_id == tax_id)
                )
            )
        )
        not_payed_users = not_payed_result.scalars().all()

        return TaxStatsSchema(
            tax_id=tax_id,
            payed=[UserSchema.model_validate(u) for u in payed_users],
            not_payed=[UserSchema.model_validate(u) for u in not_payed_users],
        )
    finally:
        await session.close()