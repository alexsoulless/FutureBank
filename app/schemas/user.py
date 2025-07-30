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

    class Config:
        orm_mode = True
    
class UserCreateSchema(BaseModel):
    username: str
    fio: str
    balance: Optional[Decimal] = Decimal(0)
    is_banned: Optional[bool] = False
    role_id: int

class UserUpdateSchema(BaseModel):
    username: Optional[str] = None
    fio: Optional[str] = None
    balance: Optional[Decimal] = None
    is_banned: Optional[bool] = None
    role_id: Optional[int] = None