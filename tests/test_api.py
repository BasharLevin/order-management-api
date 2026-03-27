from fastapi.testclient import TestClient
from app.main import app
from app import database

client = TestClient(app)


def setup_function():
    database.products.clear()
    database.orders.clear()
    database.product_id_counter = 1
    database.order_id_counter = 1


def test_create_product():
    response = client.post(
        "/products/",
        json={
            "name": "Pen",
            "price": 10.5,
            "stock": 20
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Pen"
    assert data["price"] == 10.5
    assert data["stock"] == 20


def test_get_products():
    client.post(
        "/products/",
        json={
            "name": "Pen",
            "price": 10.5,
            "stock": 20
        }
    )

    response = client.get("/products/")
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Pen"


def test_create_order_reduces_stock():
    client.post(
        "/products/",
        json={
            "name": "Pen",
            "price": 10.5,
            "stock": 20
        }
    )

    response = client.post(
        "/orders/",
        json={
            "items": [
                {
                    "product_id": 1,
                    "quantity": 2
                }
            ]
        }
    )

    assert response.status_code == 200
    order_data = response.json()
    assert order_data["total_price"] == 21
    assert order_data["status"] == "pending"

    product_response = client.get("/products/1")
    product_data = product_response.json()
    assert product_data["stock"] == 18


def test_create_order_fails_when_stock_is_too_low():
    client.post(
        "/products/",
        json={
            "name": "Pen",
            "price": 10.5,
            "stock": 2
        }
    )

    response = client.post(
        "/orders/",
        json={
            "items": [
                {
                    "product_id": 1,
                    "quantity": 5
                }
            ]
        }
    )

    assert response.status_code == 400
    assert "Not enough stock" in response.json()["detail"]


def test_update_order_status():
    client.post(
        "/products/",
        json={
            "name": "Pen",
            "price": 10.5,
            "stock": 20
        }
    )

    client.post(
        "/orders/",
        json={
            "items": [
                {
                    "product_id": 1,
                    "quantity": 2
                }
            ]
        }
    )

    response = client.put("/orders/1/status?status=completed")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "completed"