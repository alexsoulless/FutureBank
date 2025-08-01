from fastapi import APIRouter, HTTPException, Query, Path, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.schemas.tax import TaxSchema, TaxCreateSchema, TaxUpdateSchema
from app.models import Tax
from app.db import get_session

router = APIRouter(prefix="/taxes", tags=["taxes"])


@router.get("", response_model=list[TaxSchema])
async def get_taxes(session: AsyncSession = Depends(get_session)):
    try:
        result = await session.execute(select(Tax))
        taxes = result.scalars().all()
        return taxes
    finally:
        await session.close()


@router.get("/{tax_td}", response_model=list[TaxSchema])
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
