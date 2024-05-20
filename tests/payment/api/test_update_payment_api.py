import pytest
from unittest.mock import patch
from system.application.exceptions.payment_exceptions import PaymentDoesNotExistsError
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
        "type": "payment",
        "action": "payment.updated",
        "details": {
            "id": 1,
            "status": "PAID",
            "amount": 100
        }
    }

@pytest.fixture
def invalid_payment_data():
    return {"error": "invalid data"}

@pytest.fixture
def non_existing_payment_data():
    return {
        "type": "payment",
        "action": "payment.updated",
        "details": {
            "id": 999,
            "status": "PAID",
            "amount": 100
        }
    }

def test_update_payment_success(client, valid_payment_data):
    with patch('system.infrastructure.adapters.decorators.jwt_decorator.verify_token', new=mock_verify_token), \
         patch('system.infrastructure.adapters.decorators.jwt_decorator.require_auth', new=mock_require_auth), \
         patch('system.application.usecase.payment_usecase.UpdatePayment.execute') as mock_use_case:
        mock_use_case.return_value = {"success": True}
        response = client.post('/webhook/update_payment', json=valid_payment_data)
        assert response.status_code == 200

def test_update_payment_not_found(client, non_existing_payment_data):
    with patch('system.infrastructure.adapters.decorators.jwt_decorator.verify_token', new=mock_verify_token), \
         patch('system.infrastructure.adapters.decorators.jwt_decorator.require_auth', new=mock_require_auth), \
         patch('system.application.usecase.payment_usecase.UpdatePayment.execute', side_effect=PaymentDoesNotExistsError):
        response = client.post('/webhook/update_payment', json=non_existing_payment_data)
        assert response.status_code == 200
        assert response.json == {}

def test_update_payment_invalid_json(client):
    with patch('system.infrastructure.adapters.decorators.jwt_decorator.verify_token', new=mock_verify_token), \
         patch('system.infrastructure.adapters.decorators.jwt_decorator.require_auth', new=mock_require_auth):
        response = client.post('/webhook/update_payment')
        assert response.status_code == 415