from typing import List

from fastapi import APIRouter, Depends, Query

from api.schemas.bond import (
    CreatePositionRequestSchema,
    CreatePositionResponseSchema,
    ExceptionResponseSchema,
)
from api.repository.bond import BondRepository
from core.fastapi.dependencies import (
    get_current_user_id,
    PermissionDependency,
    IsAuthenticated,
    AllowAll,
    IsAdmin,
)

bond_router = APIRouter()


@bond_router.post(
    "",
    response_model=CreatePositionResponseSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
async def create_position(request: CreatePositionRequestSchema):
    # print(request.user)
    # await BondRepository().create_position(**request.dict(), )
    return {
        "name": request.name,
        "quantity": request.quantity,
        "price": request.price,
    }
