from abc import ABC, abstractmethod
from typing import List, Type

from fastapi import Request
from fastapi.openapi.models import APIKey, APIKeyIn
from fastapi.security.base import SecurityBase
from dataclasses import dataclass

from api.repository.user import UserRepository
from core.exceptions import CustomException, UnauthorizedException


class BasePermission(ABC):
    exception = CustomException

    @abstractmethod
    async def has_permission(self, request: Request) -> bool:
        pass


class IsAuthenticated(BasePermission):
    exception = UnauthorizedException

    async def has_permission(self, request: Request) -> bool:
        return request.user.id is not None


class IsAdmin(BasePermission):
    exception = UnauthorizedException

    async def has_permission(self, request: Request) -> bool:
        user_id = request.user.id
        if not user_id:
            return False

        return await UserRepository().is_admin(user_id=user_id)


class AllowAll(BasePermission):
    async def has_permission(self, request: Request) -> bool:
        return True


class PermissionDependency(SecurityBase):
    def __init__(self, permissions: List[Type[BasePermission]]):
        self.permissions = permissions
        self.model: APIKey = APIKey(
            **{"in": APIKeyIn.header},
            name="Authorization",
            description='Set "Bearer TOKEN"',
        )
        self.scheme_name = self.__class__.__name__

    async def __call__(self, request: Request):
        for permission in self.permissions:
            cls = permission()
            if not await cls.has_permission(request=request):
                raise cls.exception

    def __hash__(self):
        # FIXME find something uniq and repeatable
        return 123456

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, PermissionDependency):
            return True
        return False


async def get_current_user_id(request: Request):
    if not (user_id := request.user.id):
        raise UnauthorizedException
    return user_id
