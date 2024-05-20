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

@pytest.fixture
def valid_payment_data():
    return {
        "amount": 100,
        "payment_method": "credit_card",
        "payer_id": "123456",
        "currency": "USD"
    }

# Create a mock response class
class MockPaymentResponse:
    def __init__(self, response):
        self.response = response

def test_create_payment_success(client, valid_payment_data):
    with app.app_context():
        with patch('system.infrastructure.adapters.decorators.jwt_decorator.verify_token', new=mock_verify_token), \
             patch('system.infrastructure.adapters.decorators.jwt_decorator.require_auth', new=mock_require_auth), \
             patch('system.application.usecase.payment_usecase.CreatePayment.execute') as mock_use_case:
            mock_use_case.return_value = MockPaymentResponse({"success": True})
            response = client.post('/create_payment', json=valid_payment_data)
            assert response.status_code == 200
            assert response.json == {"success": True}

def test_create_payment_invalid_json(client):
    with app.app_context():
        with patch('system.infrastructure.adapters.decorators.jwt_decorator.verify_token', new=mock_verify_token), \
             patch('system.infrastructure.adapters.decorators.jwt_decorator.require_auth', new=mock_require_auth), \
             patch('system.application.usecase.payment_usecase.CreatePayment.execute') as mock_use_case:
            mock_use_case.return_value = MockPaymentResponse({"error": "Invalid data"})
            response = client.post('/create_payment')
            assert response.status_code == 415

def test_create_payment_internal_error(client, valid_payment_data):
    with app.app_context():
        with patch('system.infrastructure.adapters.decorators.jwt_decorator.verify_token', new=mock_verify_token), \
             patch('system.infrastructure.adapters.decorators.jwt_decorator.require_auth', new=mock_require_auth), \
             patch('system.application.usecase.payment_usecase.CreatePayment.execute', side_effect=InfrastructureError):
            response = client.post('/create_payment', json=valid_payment_data)
            assert response.status_code == 500
            assert response.json == {"error": "Internal Error"}