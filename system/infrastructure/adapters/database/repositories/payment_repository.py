from datetime import datetime
from decimal import Decimal
import random
from pymongo.errors import PyMongoError
from psycopg2 import IntegrityError
from system.application.ports.payment_port import PaymentPort
from system.domain.entities.payment import PaymentEntity
from system.domain.enums.enums import PaymentStatusEnum
from system.application.exceptions.repository_exception import DataRepositoryExeption
from uuid import uuid1
# from system.infrastructure.adapters.database.models import db
from system.infrastructure.adapters.database.models.payment_model import PaymentModel
from system.infrastructure.adapters.database.connection import Connection


db = Connection("financial")


class PaymentRepository(PaymentPort):
    @classmethod
    def create_payment(cls, value) -> PaymentEntity:
        """Create payment"""
        payment = PaymentEntity(value=str(value))
        _id=str(uuid1().hex)
        payment.id = _id
        payment_to_insert = payment.model_dump(by_alias=True)
        try:
            db.payment.insert_one(payment_to_insert)
        except PyMongoError as ex:
            raise DataRepositoryExeption(str(ex))
        return PaymentEntity.model_validate(payment_to_insert)

    @classmethod
    def update_payment_status(
        cls, payment_id: int, payment_status: PaymentStatusEnum
    ) -> PaymentEntity:
        """update payment by its id"""
        query = {"_id": payment_id}
        content = {"$set": {"status": payment_status, "status_updated_at": datetime.now()}}
        payment = db.payment.update_one(query, content)
        payment = db.payment.find_one(query)
        return PaymentEntity.model_validate(payment)
    
    @classmethod
    def update_payment_qrcode(
        cls, payment_id: int, payment_qrcode: str
    ) -> PaymentEntity:
        """update payment by its id"""
        query = {"_id": payment_id}
        content = {"$set": {"qr_code": payment_qrcode}}
        payment = db.payment.update_one(query, content)
        payment = db.payment.find_one(query)
        return PaymentEntity.model_validate(payment)

    @classmethod
    def get_payment_by_id(cls, payment_id) -> PaymentEntity:
        query = {"_id": payment_id}
        payment = db.payment.find_one(query)
        return PaymentEntity.model_validate(payment)
