from sqlalchemy import or_
from app.schemas.transaction import TransactionSchema, TransactionCreateSchema
from fastapi import APIRouter, HTTPException, Query, Path, status, Depends, Body
from app.db import get_session
from sqlalchemy.future import select
from app.models import User, Transaction
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.get("", response_model=list[TransactionSchema])
async def get_transactions(
    session: AsyncSession = Depends(get_session),
    user_id: int = Query(..., ge=1),
    offset: int = Query(0, ge=0),
    count: int = Query(15, ge=1)
):
    try:
        user_res = await session.execute(select(User).filter_by(id=user_id))
        user = user_res.scalar_one_or_none()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        query = (
                select(Transaction)
                .filter(
                    or_(
                        Transaction.sender_id == user_id,
                        Transaction.recipient_id == user_id,
                    )
                )
                .offset(offset)
                .limit(count)
            )
        query = query.order_by(Transaction.transaction_datetime.desc())
        res = await session.execute(query)
        transactions = res.scalars().all()
        return transactions
    finally:
        await session.close()
