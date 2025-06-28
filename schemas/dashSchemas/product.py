from pydantic import BaseModel, Field, UUID4, ConfigDict
from decimal import Decimal

# ===================== Product =====================

class ProductIdentifier(BaseModel):
    id: UUID4

    model_config = ConfigDict(from_attributes=True)


class Product(ProductIdentifier):
    name: str = Field(..., description="Name of the product")
    category: str = Field(..., description="Product category")
    description: str = Field(..., description="Product description")
    value: Decimal = Field(..., description="Product value")
    on_offer: bool = Field(..., description="Is the product on offer")

