from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class ProductCreate(BaseModel):
    name: str
    price: float
    stock: int

class OrderCreate(BaseModel):
    product_id: int
    quantity: int
