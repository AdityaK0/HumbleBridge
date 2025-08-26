from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from models.user import UserRole

class UserBase(BaseModel):
    email: EmailStr
    role: UserRole = UserRole.DONOR

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserProfile(BaseModel):
    id: int
    email: str
    role: UserRole
    created_at: datetime
    coins: int = 0
    pending_donations :int = 0
    delivered_donations :int = 0
    total_donations :  int = 0
    
    

    class Config:
        from_attributes = True


class UserOut(BaseModel):
    id: int
    email: str
    role: str
    created_at: datetime

    class Config:
        orm_mode = True
        from_attributes=True

class Token(BaseModel):
    access_token: str
    token_type: str
    user : UserOut

class TokenData(BaseModel):
    email: Optional[str] = None 