from fastapi import APIRouter, HTTPException
from app.schemas import ProductCreate, ProductResponse
from app import database

router = APIRouter()

#create product and store in memory
@router.post("/", response_model=ProductResponse)
def create_product(product: ProductCreate):
    new_product = {
        "id": database.product_id_counter,
        "name": product.name,
        "price": product.price,
        "stock": product.stock
    }

    database.products[database.product_id_counter] = new_product
    database.product_id_counter += 1

    return new_product

# retrieve all products
@router.get("/", response_model=list[ProductResponse])
def get_products():
    return list(database.products.values())

# retrieve product by id 
@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int):
    product = database.products.get(product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product