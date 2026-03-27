# Order Management API

A REST API built with FastAPI for managing products, orders, and basic stock handling.

---

## Features

- Create and list products
- Retrieve a product by ID
- Create orders with multiple items
- Retrieve all orders or a specific order
- Update order status (`pending`, `completed`, `cancelled`)
- Automatic stock validation
- Automatic stock deduction when orders are placed

---

## Tech Stack

- Python
- FastAPI
- Pydantic
- Uvicorn
- Pytest

---

## Project Structure

```
orderManagment_API/
├── app/
│   ├── main.py
│   ├── schemas.py
│   ├── database.py
│   └── routes/
│       ├── products.py
│       └── orders.py
├── tests/
│   └── test_api.py
├── requirements.txt
├── pytest.ini
└── README.md
```

---

## Setup & Run

### 1. Clone the repository
```bash
git clone https://github.com/BasharLevin/order-management-api.git
cd orderManagment_API
```

### 2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the application
```bash
uvicorn app.main:app --reload --port 8001
```

---

## API Documentation

Open in your browser:

http://127.0.0.1:8001/docs

Use this interface to test all endpoints.

---

## Example Requests

### Create Product
```json
{
  "name": "Pen",
  "price": 10.5,
  "stock": 20
}
```

### Create Order
```json
{
  "items": [
    {
      "product_id": 1,
      "quantity": 2
    }
  ]
}
```

---

## Running Tests

```bash
pytest
```

---

## Notes

- Uses in-memory storage for simplicity within the assignment scope
- Data resets when the server restarts

---

## Design Notes

The implementation focuses on:
- Clear API structure
- Input validation using Pydantic
- Correct business logic for stock handling
- Simple and maintainable code within the given time scope

The current design can be easily extended with a database (e.g. SQLite or PostgreSQL) without changing the API structure.