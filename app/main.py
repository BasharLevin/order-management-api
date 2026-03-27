from fastapi import FastAPI
from app.routes import products, orders

app = FastAPI()

app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(orders.router, prefix="/orders", tags=["Orders"])

@app.get("/")
def root():
    return {"message": "Order Management API is running"}