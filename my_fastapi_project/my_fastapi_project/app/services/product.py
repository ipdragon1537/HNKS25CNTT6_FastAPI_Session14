"""
services/product.py
Xử lý logic nghiệp vụ: thêm, xem, sửa, xóa sản phẩm.
Đây là tầng trung gian giữa router (nhận request) và model (bảng dữ liệu),
giúp router không phải viết trực tiếp câu lệnh truy vấn.
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


def get_all_products(db: Session):
    """Lấy toàn bộ sản phẩm trong bảng products."""
    return db.query(Product).all()


def get_product_by_id(db: Session, product_id: int) -> Product:
    """
    Tìm sản phẩm theo id.
    Nếu không tìm thấy, ném lỗi 404 để router trả về cho client.
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy sản phẩm với id = {product_id}",
        )
    return product


def create_product(db: Session, product_data: ProductCreate) -> Product:
    """Thêm sản phẩm mới vào MySQL."""
    new_product = Product(
        name=product_data.name,
        price=product_data.price,
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)  # lấy lại id vừa được MySQL sinh ra
    return new_product


def update_product(db: Session, product_id: int, product_data: ProductUpdate) -> Product:
    """
    Cập nhật thông tin sản phẩm.
    Nếu không tìm thấy sản phẩm, get_product_by_id sẽ tự ném lỗi 404.
    """
    product = get_product_by_id(db, product_id)

    product.name = product_data.name
    product.price = product_data.price

    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, product_id: int) -> None:
    """
    Xóa sản phẩm khỏi MySQL.
    Nếu không tìm thấy sản phẩm, get_product_by_id sẽ tự ném lỗi 404.
    """
    product = get_product_by_id(db, product_id)
    db.delete(product)
    db.commit()
