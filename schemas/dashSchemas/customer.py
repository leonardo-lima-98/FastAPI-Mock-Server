from pydantic import BaseModel, Field, UUID4, ConfigDict
from datetime import date

# ===================== Customer =====================

class CustomerIdentifier(BaseModel):
    id: UUID4

    model_config = ConfigDict(from_attributes=True)


class Customer(CustomerIdentifier):
    first_name: str = Field(..., description="First name of the customer")
    last_name: str = Field(..., description="Last name of the customer")
    birthday: date = Field(..., description="Birthday of the customer")
    email: str = Field(..., description="Email address of the customer")
