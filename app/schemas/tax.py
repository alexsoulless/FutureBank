from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime
from decimal import Decimal

class TaxSchema(BaseModel):
    id: int
    name: str
    due_datetime: datetime
    amount: Decimal
    
class TaxCreateSchema(TaxSchema):
    pass

class TaxUpdateSchema(TaxSchema):
    pass