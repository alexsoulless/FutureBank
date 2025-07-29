from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime
from decimal import Decimal

class TaxPaymentSchema(BaseModel):
    id: int
    user_id: int
    tax_id: int

class TaxPaymentCreateSchema(TaxPaymentSchema):
    pass