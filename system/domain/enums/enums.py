from enum import Enum


class PaymentStatusEnum(str, Enum):
    PAID = "PAID"
    UNPAID = "UNPAID"
    CANCELLED = "CANCELLED"
