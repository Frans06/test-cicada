from typing import List
from enum import Enum
from fastapi import APIRouter, Depends, Query

from api.schemas.bond import (
    CreatePositionRequestSchema,
    CreatePositionResponseSchema,
    GetBondListResponseSchema,
    BuyPositionResponseSchema,
    ExceptionResponseSchema,
)
from api.repository.bond import BondRepository
from core.fastapi.dependencies import (
    get_current_user_id,
    PermissionDependency,
    IsAuthenticated,
    AllowAll,
    IsAdmin,
    RateLimiter,
)

bond_router = APIRouter()


class CurrencyEnum(str, Enum):
    USD = "USD"
    MXN = "MXN"


@bond_router.post(
    "",
    response_model=CreatePositionResponseSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[
        Depends(PermissionDependency([IsAuthenticated])),
        Depends(RateLimiter()),
    ],
)
async def create_position(
    request: CreatePositionRequestSchema, user_id=Depends(get_current_user_id)
):
    result, _ = await BondRepository().create_position(
        **request.dict(), owner_id=user_id
    )
    return {
        "name": request.name,
        "quantity": request.quantity,
        "price": request.price,
        "id": result.id,
        "owner_id": user_id,
    }


@bond_router.get(
    "",
    response_model=List[GetBondListResponseSchema],
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[
        Depends(PermissionDependency([IsAuthenticated])),
        Depends(RateLimiter()),
    ],
)
async def list_positions(
    currency: CurrencyEnum = Query(CurrencyEnum.MXN, description="Currency"),
    limit: int = Query(10, description="Limit"),
    prev: int = Query(None, description="Prev ID"),
):
    results = await BondRepository().get_positions(limit=limit, prev=prev)
    if currency == CurrencyEnum.USD:
        results = await BondRepository.attach_exchange_rate(results)
    return results


@bond_router.patch(
    "/{id}/buy",
    response_model=BuyPositionResponseSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[
        Depends(PermissionDependency([IsAuthenticated])),
        Depends(RateLimiter()),
    ],
)
async def buy_position(id: str, buyer_id=Depends(get_current_user_id)):
    result, _ = await BondRepository().buy_position(position=id, buyer_id=buyer_id)
    return {
        "id": result.id,
        "owner_id": result.owner_id,
        "name": result.name,
        "status": result.status,
        "success": True,
    }
