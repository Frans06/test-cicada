from typing import List

from fastapi import APIRouter, Depends, Query

from api.schemas.bond import (
    CreatePositionRequestSchema,
    CreatePositionResponseSchema,
    GetBondListResponseSchema,
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
async def create_position(request: CreatePositionRequestSchema, user_id= Depends(get_current_user_id)):
    result, _ = await BondRepository().create_position(**request.dict(), owner_id=user_id )
    return {
        "name": request.name,
        "quantity": request.quantity,
        "price": request.price,
        "id": result.id,
        "owner_id": user_id
    }

@bond_router.get(
    "",
    response_model=List[GetBondListResponseSchema],
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
async def list_positions(limit: int = Query(10, description="Limit"),
    prev: int = Query(None, description="Prev ID")):
    result = await BondRepository().get_positions(limit=limit, prev=prev )
    return result
