from flask_restful import Resource
from system.application.dto.requests.payment_response import CreatePaymentResponse, GetPaymentsResponse
from system.application.exceptions.default_exceptions import InfrastructureError
from system.application.exceptions.repository_exception import DataRepositoryExeption
from system.application.usecase.usecases import UseCase
from system.domain.enums.enums import PaymentStatusEnum
from system.infrastructure.adapters.database.repositories.payment_repository import (
    PaymentRepository,
)
from system.infrastructure.adapters.external_tools.order_service import OrderService
from system.infrastructure.adapters.external_tools.mercado_pago import MercadoPago


class UpdatePayment(UseCase, Resource):
    def execute(request_json: dict) -> None:
        """
        Get order's payment status
        """

        payment_external_id = request_json.get("data", {}).get("id")
        if not payment_external_id:
            return
        payment_info = MercadoPago.get_payment_by_id(payment_external_id)
        payment = PaymentRepository.get_payment_by_id(
            payment_info["external_reference"]
        )
        if payment_info["status"] == "approved":
            PaymentRepository.update_payment_status(payment.id, PaymentStatusEnum.PAID)
            OrderService.update_order_status(payment.id, "RECEIVED")
        if payment_info["status"] in ("charged_back", "cancelled", "refunded"):
            PaymentRepository.update_payment_status(payment.id, PaymentStatusEnum.CANCELLED)
            OrderService.update_order_status(payment.id, "CANCELED")


class CreatePayment(UseCase, Resource):
    def execute(request_json: dict) -> CreatePaymentResponse:
        try:
            payment = PaymentRepository.create_payment(request_json["value"])
            pix_payment = MercadoPago.create_qr_code_pix_payment(payment.id)
            payment = PaymentRepository.update_payment_qrcode(payment.id, pix_payment["qr_data"])
        except DataRepositoryExeption as err:
            raise InfrastructureError(str(err))
        return CreatePaymentResponse(payment.model_dump())


class GetPayments(UseCase, Resource):
    def execute() -> GetPaymentsResponse:
        try:
            payments = PaymentRepository.get_payments()
        except DataRepositoryExeption as err:
            raise InfrastructureError(str(err))
        return GetPaymentsResponse({"payments": [payment.model_dump() for payment in payments]}) 
        
        
