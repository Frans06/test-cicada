from pydantic import BaseModel, Field, EmailStr, validator, condecimal
from core.fastapi.schemas.current_user import CurrentUser
from db.models.bond import BondStatus

class CreatePositionRequestSchema(BaseModel):
    name: str = Field(..., description="Name", min_length=3, max_length=40)
    quantity: int = Field(...,le=10000, gt=0,  description="quantity")
    price: condecimal(gt= 0, le= 100000000, max_digits=13, decimal_places=4) = Field(
        ..., description="Quantity"
    )

class CreatePositionResponseSchema(BaseModel):
    id: int = Field(..., description="position Id")
    quantity: int = Field(...,le=10000, gt=0,  description="quantity")
    owner_id: int = Field(..., description="Owner Id")
    price: condecimal(gt= 0, le= 100000000, max_digits=13, decimal_places=4) = Field(
        ..., description="Quantity"
    )
    name: str = Field(..., description='Bond name')
    class Config:
        orm_mode = True

class GetBondListResponseSchema(BaseModel):
    id: int = Field(..., description="position Id")
    quantity: int = Field(...,le=10000, gt=0,  description="quantity")
    owner_id: int = Field(..., description="Owner Id")
    price: condecimal() = Field(
        ..., description="Quantity"
    )
    status: BondStatus = Field(..., description="position status")
    name: str = Field(..., description='Bond name')    
    class Config:
        orm_mode = True

class ExceptionResponseSchema(BaseModel):
    error: str
