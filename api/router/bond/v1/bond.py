from typing import List

from fastapi import APIRouter, Depends, Query

from api.schemas.bond import (
    CreatePositionRequestSchema,
    CreatePositionResponseSchema,
    ExceptionResponseSchema,
)
from api.repository.bond import BondRepository
from core.fastapi.dependencies import (
    PermissionDependency,
    IsAdmin,
)

bond_router = APIRouter()


@bond_router.post(
    "",
    response_model=CreatePositionResponseSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def create_position(request: CreatePositionRequestSchema):
    print(request)
    await BondRepository().create_position(**request.dict())
    return {
        id: request.id,
        name: request.name,
        quantity: request.quantity,
        price: request.price,
    }
