from typing import Optional, List, Tuple
from decimal import localcontext
from sqlalchemy import or_, select, and_, update

from db.models import Bond, BondStatus, Transaction, TransactionType
from api.schemas.bond import BondSchema
from core.db import Transactional, session
from core.exceptions import (
    PasswordDoesNotMatchException,
    DuplicateEmailOrNicknameException,
    UserNotFoundException,
    BondAlreadySoldException,
    SameUserBuyException,
)
from core.utils.token_helper import TokenHelper
from core.external import get_exchange_rate


class BondRepository:
    def __init__(self):
        ...

    @Transactional()
    async def create_position(
        self, owner_id: int, name: int, quantity: int, price: str
    ) -> None:
        bond = Bond(name=name, quantity=quantity, owner_id=owner_id, price=price)
        session.add(bond)
        return bond

    async def get_positions(
        self, limit: int = 12, prev: Optional[int] = None
    ) -> List[Bond]:
        query = select(Bond)

        if prev:
            query = query.where(Bond.id > prev)

        if limit > 12:
            limit = 12

        query = query.limit(limit)
        result = await session.execute(query)
        return result.scalars().all()

    @Transactional()
    async def buy_position(self, position: int, buyer_id: int) -> List[Bond]:
        result = await session.execute(select(Bond).where(position == Bond.id))
        bond = result.scalar_one()
        print(bond.status, BondStatus.sold, position)
        if bond.status == BondStatus.sold:
            raise BondAlreadySoldException
        if bond.owner_id == buyer_id:
            raise SameUserBuyException
        query = (
            update(Bond)
            .where(Bond.id == position)
            .values(status=BondStatus.sold, owner_id=buyer_id)
        )
        await session.execute(query)
        sell_trans = Transaction(
            bond_id=bond.id,
            user_id=bond.owner_id,
            transaction_type=TransactionType.sell,
        )
        buy_trans = Transaction(
            bond_id=bond.id, user_id=bond.owner_id, transaction_type=TransactionType.buy
        )
        session.add(sell_trans)
        session.add(buy_trans)
        return bond

    @staticmethod
    async def attach_exchange_rate(results: List[Bond]):
        rate = await get_exchange_rate()
        new_result = []
        for bond in results:
            with localcontext() as ctx:
                ctx.prec = 4
                new_price = bond.price / rate
                new_bond = BondSchema.from_orm(bond)
                new_bond.price = new_price
                new_result.append(new_bond)
        return new_result
