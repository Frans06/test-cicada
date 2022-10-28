from typing import Optional, List

from sqlalchemy import or_, select, and_

from db.models import Bond
from api.schemas.user import LoginResponseSchema
from core.db import Transactional, session
from core.exceptions import (
    PasswordDoesNotMatchException,
    DuplicateEmailOrNicknameException,
    UserNotFoundException,
)
from core.utils.token_helper import TokenHelper


class BondRepository:
    def __init__(self):
        ...

    @Transactional()
    async def create_position(self, owner_id: int, name: int, quantity: int) -> None:
        bond = Bond(name=name, quantity=quantity, owner_id=owner_id)
        session.add(bond)
