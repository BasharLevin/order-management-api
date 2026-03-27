from fastapi import APIRouter, HTTPException
from app.schemas import OrderCreate, OrderResponse
from app import database

router = APIRouter()


@router.post("/", response_model=OrderResponse)
def create_order(order: OrderCreate):
    order_items_response = []
    total_price = 0.0

    for item in order.items:
        product = database.products.get(item.product_id)

        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")

        if item.quantity > product["stock"]:
            raise HTTPException(
                status_code=400,
                detail=f"Not enough stock for product {product['name']}"
            )

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

    new_order = {
        "id": database.order_id_counter,
        "items": order_items_response,
        "total_price": total_price,
        "status": "pending"
    }

    database.orders[database.order_id_counter] = new_order
    database.order_id_counter += 1

    return new_order


@router.get("/", response_model=list[OrderResponse])
def get_orders():
    return list(database.orders.values())


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int):
    order = database.orders.get(order_id)

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return order