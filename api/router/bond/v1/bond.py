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


"""
It creates a bond position

:param request: CreatePositionRequestSchema - this is the request body that will be validated
against the schema
:type request: CreatePositionRequestSchema
:param user_id: This is the user_id that we get from the get_current_user_id function
:return: The response is a dict with the following keys:
    name: str
    quantity: int
    price: float
    id: int
    owner_id: int
"""


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


"""
It returns a list of bond positions, optionally filtered by currency and paginated by limit and prev

:param currency: CurrencyEnum = Query(CurrencyEnum.MXN, description="Currency")
:type currency: CurrencyEnum
:param limit: int = Query(10, description="Limit")
:type limit: int
:param prev: int = Query(None, description="Prev ID")
:type prev: int
:return: A list of bonds
"""


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


"""
"Buy a bond position."
:param id: str - the id of the position to buy
:type id: str
:param buyer_id: The ID of the user who is buying the position
:return: A dictionary with the id, owner_id, name, status, and success of the bond.
"""


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
