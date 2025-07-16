from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Product

router = APIRouter()
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/product", response_class=HTMLResponse)
def get_products(request: Request, db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return templates.TemplateResponse("products.html", {"request": request, "products": products})

@router.post("/add_product")
def add_product(name: str = Form(...), price: float = Form(...), stock: int = Form(...), db: Session = Depends(get_db)):
    new_product = Product(name=name, price=price, stock=stock)
    db.add(new_product)
    db.commit()
    return RedirectResponse("/products", status_code=302)
