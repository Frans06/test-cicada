from pydantic import BaseModel, Field, EmailStr, validator, condecimal


class CreatePositionRequestSchema(BaseModel):
    name: str = Field(..., description="Name", min_length=3, max_length=40)
    quantity: condecimal(max_digits=13, decimal_places=4) = Field(
        ..., description="Quantity"
    )
    price: str = Field(..., description="Price")


class CreatePositionResponseSchema(BaseModel):
    id: int = Field(..., description="position Id")
    quantity: str = Field(..., description="quantity")
    owner_id: int = Field(..., description="Owner Id")
    price: condecimal(max_digits=13, decimal_places=4) = Field(
        ..., description="Quantity"
    )

    class Config:
        orm_mode = True


class ExceptionResponseSchema(BaseModel):
    error: str
