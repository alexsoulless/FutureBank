from sqlalchemy import or_
from app.schemas.transaction import TransactionSchema, TransactionCreateSchema
from fastapi import APIRouter, HTTPException, Query, Path, status, Depends, Body
from app.db import get_session
from sqlalchemy.future import select
from app.models import User, Transaction
from sqlalchemy.ext.asyncio import AsyncSession
from decimal import Decimal
from datetime import datetime


router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.get("", response_model=list[TransactionSchema])
async def get_transactions(
    user_id: int = Query(..., ge=1),
    offset: int = Query(0, ge=0),
    count: int = Query(15, ge=1),
    session: AsyncSession = Depends(get_session),
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


@router.post("")
async def make_transaction(
    sender_id: int = Query(..., ge=1),
    recipient_id: int = Query(..., ge=1),
    amount: Decimal = Query(..., gt=0),
    forced: bool = Query(False),
    session: AsyncSession = Depends(get_session),
) -> TransactionSchema:
    """Выполнение транзакции с занесением в базу данных

    Args:
        sender_id (int, optional): id отправителя. Defaults to Query(..., ge=1).
        recipient_id (int, optional): id получателя. Defaults to Query(..., ge=1).
        amount (Decimal, optional): сумма транзакции. Defaults to Query(..., gt=0).
        forced (bool, optional): усиленна ли транзакция. Defaults to Query(False).

    Raises:
        HTTPException 400 (extra_code=1): отправитель и получатель один и тот же
        HTTPException 404 (extra_code=2): нет такого отправителя
        HTTPException 404 (extra_code=3): нет такого получателя
        HTTPException 402 (extra_code=4): недостаточно средств у отправителя и транзакция не усилена

    Returns:
        TransactionSchema: транзакция
    """
    try:
        if sender_id == recipient_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Sender and recipient cannot be the same",
                headers={"extra_code": "1"},
            )

        sender_res = await session.execute(select(User).filter_by(id=sender_id))
        sender = sender_res.scalar_one_or_none()
        if sender is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cant find sender",
                headers={"extra_code": "2"},
            )

        recipient_res = await session.execute(select(User).filter_by(id=recipient_id))
        recipient = recipient_res.scalar_one_or_none()

        if recipient is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cant find recipient_id",
                headers={"extra_code": "3"},
            )

        if sender.balance < amount and not forced: # type: ignore
            raise HTTPException(
                status_code=status.HTTP_402_PAYMENT_REQUIRED,
                detail="Not enough money",
                headers={"extra_code": "4"},
            )

        sender.balance -= amount # type: ignore
        recipient.balance += amount # type: ignore

        transaction = Transaction(
            sender_id=sender_id,
            recipient_id=recipient_id,
            amount=amount,
            transaction_datetime=datetime.now(),
        )

        session.add(transaction)
        await session.commit()
        await session.refresh(transaction)
        return transaction
    except Exception as ex:
        await session.rollback()
        raise ex
    finally:
        await session.close()
