from pydantic import BaseModel, Field, UUID4, ConfigDict
from datetime import date

# ===================== Purchase =====================

class PurchaseIdentifier(BaseModel):
    id: UUID4

    model_config = ConfigDict(from_attributes=True)


class Purchase(PurchaseIdentifier):
    customer_id: UUID4 = Field(..., description="Customer who made the purchase")
    product_id: UUID4 = Field(..., description="Product that was purchased")
    purchase_date: date = Field(..., description="Date of the purchase")
