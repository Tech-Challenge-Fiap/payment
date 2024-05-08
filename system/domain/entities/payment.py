from decimal import Decimal
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from system.domain.enums.enums import PaymentStatusEnum


class PaymentEntity(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    qr_code: Optional[str] = None
    status_updated_at: Optional[datetime] = None
    status: PaymentStatusEnum = PaymentStatusEnum.UNPAID
    value: str

    class Config:
        from_attributes = True
        use_enum_values = True
