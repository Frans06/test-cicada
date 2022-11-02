from typing import List

from fastapi import APIRouter, Depends, Query

from api.schemas.user import (
    LoginRequest,
    LoginResponse,
    ExceptionResponseSchema,
    CreateUserRequestSchema,
    GetUserListResponseSchema,
    CreateUserResponseSchema,
)
from api.repository.user import UserRepository
from core.fastapi.dependencies import PermissionDependency, IsAdmin, RateLimiter

user_router = APIRouter()


"""
"Get a list of users."

The first line of the function is the route. It's a GET request to the /users endpoint

:param limit: int = Query(10, description="Limit")
:type limit: int
:param prev: int = Query(None, description="Prev ID")
:type prev: int
:return: A list of user objects
"""


@user_router.get(
    "",
    response_model=List[GetUserListResponseSchema],
    response_model_exclude={"id"},
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([IsAdmin])), Depends(RateLimiter())],
)
async def get_user_list(
    limit: int = Query(10, description="Limit"),
    prev: int = Query(None, description="Prev ID"),
):
    return await UserRepository().get_user_list(limit=limit, prev=prev)


"""
"Create a user with the given email and nickname."

:param request: CreateUserRequestSchema
:type request: CreateUserRequestSchema
:return: CreateUserResponseSchema
"""


@user_router.post(
    "",
    response_model=CreateUserResponseSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(RateLimiter())],
)
async def create_user(request: CreateUserRequestSchema):
    await UserRepository().create_user(**request.dict())
    return {"email": request.email, "nickname": request.nickname}


"""
This function takes a LoginRequest object, calls the login function in the UserRepository, and
returns a LoginResponse object.

:param request: LoginRequest - this is the request body that will be validated against the
LoginRequest schema
:type request: LoginRequest
:return: A LoginResponse object with the token and refresh_token
"""


@user_router.post(
    "/login",
    response_model=LoginResponse,
    responses={"404": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(RateLimiter())],
)
async def login(request: LoginRequest):
    token = await UserRepository().login(email=request.email, password=request.password)
    return {"token": token.token, "refresh_token": token.refresh_token}
