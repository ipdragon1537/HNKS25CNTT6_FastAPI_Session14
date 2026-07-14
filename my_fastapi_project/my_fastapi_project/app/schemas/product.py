from pydantic import BaseModel, Field, ConfigDict
class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Tên sản phẩm")
    price: float = Field(..., gt=0, description="Giá sản phẩm, phải lớn hơn 0")
class ProductCreate(ProductBase):
    pass
class ProductUpdate(ProductBase):
    pass
class ProductResponse(ProductBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
