import json
import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient

test_orders = [
    {
        "created_at": "2016-01-17T17:02:25.660Z",
        "description": "Test order 1",
        "title": "fugiat magna Lorem aliquip qui",
        "customer": {
            "billing_address": {
                "postcode": "MO73 2ID",
                "county": "Westmorland",
                "city": "Oley",
                "street": "124 Veranda Place"
            },
            "shipping_address": {
                "postcode": "MO73 2ID",
                "county": "Westmorland", 
                "city": "Oley",
                "street": "124 Veranda Place"
            },
            "phone": "+447482939767",
            "email": "ingrid.rios@example.com",
            "name": {
                "last": "Rios",
                "first": "Ingrid"
            }
        },
        "currency": "USD",
        "price": "0.33",
        "url": "https://example.com/products/5889b0a6797714883c501c23",
        "index": 13,
        "uuid": "30906bb3-ff12-4517-a9ea-71bb2ed79c0e",
        "id": "5889b0a6797714883c501c23"
    },
    {
        "created_at": "2016-11-22T13:06:15.868Z",
        "description": "Test order 2", 
        "title": "duis tempor consectetur aute nisi",
        "customer": {
            "billing_address": {
                "postcode": "SD97 6AZ",
                "county": "Staffordshire",
                "city": "Hardyville",
                "street": "98 Harman Street"
            },
            "shipping_address": {
                "postcode": "SD97 6AZ",
                "county": "Staffordshire",
                "city": "Hardyville", 
                "street": "98 Harman Street"
            },
            "phone": "+447748253848",
            "email": "elaine.velazquez@example.com",
            "name": {
                "last": "Velazquez",
                "first": "Elaine"
            }
        },
        "currency": "GBP",
        "price": "2.96",
        "url": "https://example.com/products/5889b0a6664152cb6bccad04",
        "index": 14,
        "uuid": "08274ee9-72e0-4a3f-a9dd-3507e87c7430",
        "id": "5889b0a6664152cb6bccad04"
    }
]

# Patch the file reading before importing main - uses fake data
with patch('builtins.open'), patch('json.load', return_value=test_orders):
    from main import app, valid_order_id

@pytest.fixture
def client():
    return TestClient(app)

# Test the helper function
def test_valid_order_id():
    assert valid_order_id("5889b0a6797714883c501c23") == True
    assert valid_order_id("abc123") == True
    assert valid_order_id("xyz") == False

# Basic API tests
def test_no_filters_returns_error(client):
    response = client.get("/api/orders")
    assert response.status_code == 400

def test_get_by_id(client):
    response = client.get("/api/orders?id=5889b0a6797714883c501c23")
    assert response.status_code == 200
    data = response.json()
    assert data["results"] == 1

def test_get_by_currency_usd(client):
    response = client.get("/api/orders?currency=USD")
    assert response.status_code == 200
    data = response.json()
    assert data["results"] == 1

def test_get_by_currency_gbp(client):
    response = client.get("/api/orders?currency=GBP")
    assert response.status_code == 200
    data = response.json()
    assert data["results"] == 1

def test_get_by_cost_low(client):
    response = client.get("/api/orders?cost=1.0")
    assert response.status_code == 200
    data = response.json()
    assert data["results"] == 1  # Only GBP order (2.96) >= 1.0

def test_get_by_cost_very_low(client):
    response = client.get("/api/orders?cost=0.1")
    assert response.status_code == 200
    data = response.json()
    assert data["results"] == 2  # Both orders >= 0.1

def test_get_by_shipped_to_city(client):
    response = client.get("/api/orders?shipped_to=Oley")
    assert response.status_code == 200
    data = response.json()
    assert data["results"] == 1

def test_get_by_shipped_to_county(client):
    response = client.get("/api/orders?shipped_to=Staffordshire")
    assert response.status_code == 200
    data = response.json()
    assert data["results"] == 1

def test_invalid_order_id(client):
    response = client.get("/api/orders?id=invalid")
    assert response.status_code == 400

def test_no_results_found(client):
    response = client.get("/api/orders?currency=JPY")
    assert response.status_code == 404

def test_high_cost_filter(client):
    response = client.get("/api/orders?cost=10.0")
    assert response.status_code == 404  # No orders >= 10.0