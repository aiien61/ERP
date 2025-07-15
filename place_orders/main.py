from fastapi import FastAPI, Depends, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.middleware.sessions import SessionMiddleware
import uvicorn

from database import SessionLocal, engine
from models import Base, Product, Order, User
from auth import router as auth_router
from products import router as product_router
from orders import router as order_router

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="erp_admin")
templates = Jinja2Templates(directory="templates")

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.include_router(auth_router)
app.include_router(product_router)
app.include_router(order_router)


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)):
    if not request.session.get("user_id"):
        return RedirectResponse("/login")
    products = db.query(Product).all()
    orders = db.query(Order).order_by(Order.id.desc()).limit(5).all()
    return templates.TemplateResponse("dashboard.html", 
                                      {"request": request, "products": products, "orders": orders})


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
