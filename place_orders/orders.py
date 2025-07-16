from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Order, Product, User

router = APIRouter()
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/orders", response_class=HTMLResponse)
def orders_page(request: Request, db: Session = Depends(get_db)):
    if not request.session.get("user_id"):
        return RedirectResponse("/login")
    products = db.query(Product).all()
    orders = db.query(Order).all()
    return templates.TemplateResponse("orders.html", {"request": request, "products": products, "orders": orders})

@router.post("/sell_product")
def sell_product(request: Request, product_id: int = Form(...), quantity: int = Form(...), db: Session = Depends(get_db)):
    if not request.session.get("user_id"):
        return RedirectResponse("/login")
    product = db.query(Product).get(product_id)
    if product and product.stock >= quantity:
        total_price: float = product.price * quantity
        product.stock -= quantity
        order = Order(product_id=product_id, quantity=quantity, total_price=total_price, user_id=request.session["user_id"])
        db.add(order)
        db.commit()
    return RedirectResponse("/orders", status_code=302)
