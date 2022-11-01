from fastapi import APIRouter, Response, Depends
from api.schemas.auth import (
    RefreshTokenRequest,
    VerifyTokenRequest,
    RefreshTokenResponse,
)
from api.repository.jwt import JwtService
from api.schemas.user import ExceptionResponseSchema
from core.fastapi.dependencies import RateLimiter

auth_router = APIRouter()


@auth_router.post(
    "/refresh",
    response_model=RefreshTokenResponse,
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(RateLimiter())],
)
async def refresh_token(request: RefreshTokenRequest):
    token = await JwtService().create_refresh_token(
        token=request.token, refresh_token=request.refresh_token
    )
    return {"token": token.token, "refresh_token": token.refresh_token}


@auth_router.post("/verify")
async def verify_token(request: VerifyTokenRequest):
    await JwtService().verify_token(token=request.token)
    return Response(status_code=200)
