from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime
from decimal import Decimal

class UserSchema(BaseModel):
    id: int
    username: str
    fio: str
    balance: Decimal
    is_banned: bool
    role_id: int

class TransactionSchema(BaseModel):
    id: int
    sender_id: int
    recipient_id: int
    transaction_datetime: datetime
    amount: Decimal

class TaxPaymentSchema(BaseModel):
    id: int
    user_id: int
    tax_id: int

class TaxSchema(BaseModel):
    id: int
    name: str
    due_datetime: datetime
    amount: Decimal

class UserUpdateSchema(BaseModel):
    username: Optional[str] = Field(None, description="Username of the user")
    FIO: Optional[str] = Field(None, description="Full name of the user")
    balance: Optional[Decimal] = Field(None, description="Balance of the user")
    is_banned: Optional[bool] = Field(None, description="Banned status of the user")
    is_org: Optional[bool] = Field(None, description="Organization status of the user")
