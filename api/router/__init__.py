from fastapi import APIRouter

from api.router.user.v1.user import user_router as user_v1_router
from api.router.auth.auth import auth_router
from api.router.bond.v1.bond import bond_router as bond_v1_router

router = APIRouter()
router.include_router(user_v1_router, prefix="/api/v1/users", tags=["User"])
router.include_router(auth_router, prefix="/auth", tags=["Auth"])
router.include_router(bond_v1_router, prefix="/api/v1/bonds", tags=["Bond"])

__all__ = ["router"]
