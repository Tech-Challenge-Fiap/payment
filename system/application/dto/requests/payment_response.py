from datetime import datetime
from typing import List, Optional
from decimal import Decimal
from flask import Response

from system.domain.enums.enums import PaymentStatusEnum

class Payment(Response):
    order_id: int
    qr_code: str
    status_updated_at: datetime
    status: PaymentStatusEnum
    value: Decimal

    class Config:
        from_attributes = True
        use_enum_values = True


class CreatePaymentResponse(Payment):
    pass


class GetPaymentsResponse(Response):
    payments: List[Payment]
