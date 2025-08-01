from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime
from decimal import Decimal
from app.schemas.user import UserSchema


class TaxPaymentCreateSchema(BaseModel):
    user_id: int
    tax_id: int


class TaxPaymentSchema(TaxPaymentCreateSchema):
    id: int


class TaxStatsSchema(BaseModel):
    payed: list[UserSchema]
    not_payed: list[UserSchema]
