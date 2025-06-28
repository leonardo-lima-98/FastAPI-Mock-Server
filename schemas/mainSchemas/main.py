from pydantic import BaseModel, Field
from typing import Any

class mainResponse(BaseModel):
    """Model for the main response structure."""
    message: str | Any | None = Field(None, description="Response message")
    status: str | Any | None = Field(None, description="HTTP status code as a string")
    data: str | Any | None = Field(None, description="List of customers if applicable")
    error: str | Any | None = Field(None, description="Error message if applicable")
    additional_info: str | Any | None = Field(None, description="Any additional information related to the response")