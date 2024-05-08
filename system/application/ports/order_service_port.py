from abc import abstractmethod


class OrderServicePort:
    @classmethod
    @abstractmethod
    def update_order_status(cls, payment_id) -> str:
        """
        Update Order Status
        """
