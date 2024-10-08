from sqlalchemy.orm import relationship
from sqlalchemy import Enum as SQLAlchemyEnum
from system.domain.enums.enums import PaymentStatusEnum
from . import db


class PaymentModel(db.Model):
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.String)
    qr_code = db.Column(db.String, nullable=True)
    status_updated_at = db.Column(db.DateTime(timezone=True))
    status = db.Column(SQLAlchemyEnum(PaymentStatusEnum), nullable=False)
    value = db.Column(db.Numeric(4, 2))
