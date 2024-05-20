# tests/features/get_payments.feature

Feature: Get payments

  Scenario: Valid get payments request
    Given the Flask app is running
    When I send a GET request to "/get_payments"
    Then the response status code should be 200
    And the response should contain a list of payments

  Scenario: Internal server error
    Given the Flask app is running
    When I send a GET request to "/get_payments" and an internal error occurs
    Then the response status code should be 500
    And the response should contain "Internal Error"