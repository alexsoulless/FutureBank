from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime
from decimal import Decimal


class TaxSchema(BaseModel):
    id: int
    name: str
    due_datetime: datetime
    amount: Decimal


class TaxCreateSchema(BaseModel):
    name: str
    due_datetime: datetime
    amount: Optional[Decimal] = Decimal("0.00")


class TaxUpdateSchema(BaseModel):
    name: Optional[str] = None
    due_datetime: Optional[datetime] = None
    amount: Optional[Decimal] = None
