import pytest
from unittest.mock import patch
from system.application.exceptions.default_exceptions import InfrastructureError
from app import app

# Mock decorators and functions
def mock_require_auth(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

def mock_verify_token(token):
    return {'user_id': '12345'}

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# Create a mock response class
class MockPaymentResponse:
    def __init__(self, response):
        self.response = response

def test_get_payments_success(client):
    with app.app_context():
        with patch('system.infrastructure.adapters.decorators.jwt_decorator.verify_token', new=mock_verify_token), \
             patch('system.infrastructure.adapters.decorators.jwt_decorator.require_auth', new=mock_require_auth), \
             patch('system.application.usecase.payment_usecase.GetPayments.execute') as mock_use_case:
            mock_use_case.return_value = MockPaymentResponse({"payments": [{"id": 1, "amount": 100}]})
            response = client.get('/get_payments')
            assert response.status_code == 200
            assert response.json == {"payments": [{"id": 1, "amount": 100}]}

def test_get_payments_internal_error(client):
    with app.app_context():
        with patch('system.infrastructure.adapters.decorators.jwt_decorator.verify_token', new=mock_verify_token), \
             patch('system.infrastructure.adapters.decorators.jwt_decorator.require_auth', new=mock_require_auth), \
             patch('system.application.usecase.payment_usecase.GetPayments.execute', side_effect=InfrastructureError):
            response = client.get('/get_payments')
            assert response.status_code == 500
            assert response.json == {"error": "Internal Error"}