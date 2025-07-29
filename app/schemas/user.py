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
    
class UserCreateSchema(UserSchema):
    pass

class UserUpdateSchema(UserSchema):
    pass