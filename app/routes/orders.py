from fastapi import APIRouter, HTTPException
from app.schemas import OrderCreate, OrderResponse
from app import database
from typing import Literal

router = APIRouter()


@router.post("/", response_model=OrderResponse)
def create_order(order: OrderCreate):
    order_items_response = []
    total_price = 0.0
    # product validation (stock and exist)
    for item in order.items:
        product = database.products.get(item.product_id)

        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")

        if item.quantity > product["stock"]:
            raise HTTPException(
                status_code=400,
                detail=f"Not enough stock for product {product['name']}"
            )
    # calculate total price
    for item in order.items:
        product = database.products[item.product_id]
        product["stock"] -= item.quantity

        line_total = product["price"] * item.quantity
        total_price += line_total

        order_items_response.append({
            "product_id": item.product_id,
            "quantity": item.quantity,
            "unit_price": product["price"],
            "line_total": line_total
        })
    # create and store the order
    new_order = {
        "id": database.order_id_counter,
        "items": order_items_response,
        "total_price": total_price,
        "status": "pending"
    }

    database.orders[database.order_id_counter] = new_order
    database.order_id_counter += 1

    return new_order


# Retrieve all orders
@router.get("/", response_model=list[OrderResponse])
def get_orders():
    return list(database.orders.values())

# Retrieve order by ID
@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int):
    order = database.orders.get(order_id)

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return order

# Update the status of an existing order
@router.put("/{order_id}/status", response_model=OrderResponse)
def update_order_status(order_id: int, status: Literal["pending", "completed", "cancelled"]):
    order = database.orders.get(order_id)

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order["status"] = status
    return order