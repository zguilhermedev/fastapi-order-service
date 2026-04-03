from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field

class CustomerCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=120)
    email: EmailStr

class CustomerResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)