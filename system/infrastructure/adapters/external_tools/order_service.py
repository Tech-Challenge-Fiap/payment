from system.application.ports.order_service_port import OrderServicePort
import requests
import json


class OrderService(OrderServicePort):
    @classmethod
    def update_order_status(cls, payment_id, status) -> str:
        """
        Update order status
        """
        url = "orderservice:5000/patch_order_by_payment"
        payload = json.dumps({
            "payment_id": payment_id,
            "status": status
        })
        response = requests.request("PATCH", url, json=payload)
        return response.json()
