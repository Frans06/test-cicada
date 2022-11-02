from typing import Optional, List

from sqlalchemy import or_, select, and_

from db.models import User
from api.schemas.user import LoginResponseSchema
from core.db import Transactional, session
from core.exceptions import (
    PasswordDoesNotMatchException,
    DuplicateEmailOrNicknameException,
    UserNotFoundException,
)
from core.utils.token_helper import TokenHelper


class UserRepository:
    def __init__(self):
        ...

    """
    `get_user_list` returns a list of `User` objects, with a maximum of 12 items, starting from the user
    with the id greater than `prev`
    
    :param limit: The number of users to return, defaults to 12
    :type limit: int (optional)
    :param prev: Optional[int] = None
    :type prev: Optional[int]
    :return: A list of User objects
    """

    async def get_user_list(
        self,
        limit: int = 12,
        prev: Optional[int] = None,
    ) -> List[User]:
        query = select(User)

        if prev:
            query = query.where(User.id > prev)

        if limit > 12:
            limit = 12

        query = query.limit(limit)
        result = await session.execute(query)
        return result.scalars().all()

    """
    > It checks if the email or nickname is already taken, and if not, it creates a new user
    
    :param email: str
    :type email: str
    :param password: The password to be hashed
    :type password: str
    :param nickname: str
    :type nickname: str
    """

    @Transactional()
    async def create_user(self, email: str, password: str, nickname: str) -> None:

        query = select(User).where(or_(User.email == email, User.nickname == nickname))
        result = await session.execute(query)
        is_exist = result.scalars().first()
        if is_exist:
            raise DuplicateEmailOrNicknameException

        user = User(email=email, password=password, nickname=nickname)
        session.add(user)

    """
    "Return True if the user with the given ID is an admin, otherwise return False."
    
    :param user_id: The user's ID
    :type user_id: int
    :return: A boolean value.
    """

    async def is_admin(self, user_id: int) -> bool:
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalars().first()
        if not user:
            return False

        if user.is_admin is False:
            return False

        return True

    """
    A login function that takes in an email and password and returns a token and refresh token.
    
    :param email: The email address of the user
    :type email: str
    :param password: The password to be hashed
    :type password: str
    :return: A LoginResponseSchema object
    """

    async def login(self, email: str, password: str) -> LoginResponseSchema:
        result = await session.execute(
            select(User).where(and_(User.email == email, password == password))
        )
        # breakpoint()
        user = result.scalars().first()
        if not user:
            raise UserNotFoundException

        response = LoginResponseSchema(
            token=TokenHelper.encode(payload={"user_id": user.id}),
            refresh_token=TokenHelper.encode(payload={"sub": "refresh"}),
        )
        return response
