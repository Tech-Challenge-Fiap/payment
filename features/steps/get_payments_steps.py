# tests/features/steps/get_payments_steps.py

from behave import when, then
import json
from unittest.mock import patch
from system.application.usecase import payment_usecase

@when('I send a GET request to "/get_payments"')
def step_impl(context):
    context.response = context.client.get("/get_payments")

@when('I send a GET request to "/get_payments" and an internal error occurs')
def step_impl(context):
    with patch.object(payment_usecase.GetPayments, 'execute', side_effect=InfrastructureError):
        context.response = context.client.get("/get_payments")

@then('the response status code should be {expected_status_code:d}')
def step_impl(context, expected_status_code):
    assert context.response.status_code == expected_status_code

@then('the response should contain a list of payments')
def step_impl(context):
    response_data = context.response.get_json()
    assert isinstance(response_data, list), "Response is not a list"

@then('the response should contain "Internal Error"')
def step_impl(context):
    response_data = context.response.get_json()
    assert "Internal Error" in response_data.get("error", "")