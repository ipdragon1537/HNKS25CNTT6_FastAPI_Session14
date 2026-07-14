from fastapi import FastAPI
from app.database import engine, Base
from app.models import product as product_model  # noqa: F401 (import để Base biết bảng products)
from app.routers import product as product_router
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(product_router.router)
@app.get("/")
def root():
    return {"message": "Product Management API is running"}
