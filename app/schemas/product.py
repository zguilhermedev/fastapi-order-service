from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=120)
    description: str | None = None
    price: Decimal = Field(..., gt=0)


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str | None
    price: Decimal
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)