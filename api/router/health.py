from fastapi import APIRouter, Response, Depends
from core.fastapi.dependencies import PermissionDependency, AllowAll, RateLimiter

health_router = APIRouter()


@health_router.get(
    "/health",
    dependencies=[
        Depends(PermissionDependency([AllowAll])),
        Depends(RateLimiter()),
    ],
)
async def home():
    return Response(status_code=200)
