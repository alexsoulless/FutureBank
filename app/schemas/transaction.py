from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime
from decimal import Decimal

class TransactionSchema(BaseModel):
    id: int
    sender_id: int
    recipient_id: int
    transaction_datetime: datetime
    amount: Decimal
    
class TransactionCreateSchema(TransactionSchema):
    pass

class TransactionUpdateSchema(TransactionSchema):
    pass