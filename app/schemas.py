from pydantic import BaseModel, Field
from typing import List, Literal 


class ProductCreate(BaseModel):
    name: str 
    price: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)
    

class ProductResponse(BaseModel):
    id: int 
    name: str
    price: float 
    stock: int 
    
class OrderItemCreate(BaseModel): 
    product_id: int 
    quantity: int = Field(...,gt = 0)
    
    
class OrderCreate(BaseModel):
    items: List[OrderItemCreate]
    

class OrderItemResponse(BaseModel):    
    product_id: int
    quantity: int
    unit_price: float
    line_total: float
    
    
class OrderResponse(BaseModel):
    id: int
    items: List[OrderItemResponse]
    total_price: float
    status: Literal["pending", "completed", "cancelled"]