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
    async def create_position(self, owner_id: int, name: int, quantity: int, price: str) -> None:
        bond = Bond(name=name, quantity=quantity, owner_id=owner_id, price= price)
        session.add(bond)
        return bond
    
    async def get_positions(self, limit: int = 12, prev: Optional[int] = None) -> List[Bond]:
        query = select(Bond)

        if prev:
            query = query.where(Bond.id > prev)

        if limit > 12:
            limit = 12

        query = query.limit(limit)
        result = await session.execute(query)
        return result.scalars().all()
