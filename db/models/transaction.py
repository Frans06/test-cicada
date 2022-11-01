import uuid
import enum
from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, BigInteger, Enum
from sqlalchemy.orm import relationship

from core.db import Base
from core.db.mixins import TimestampMixin

if TYPE_CHECKING:
    from .bond import Bond  # noqa: F401


class TransactionType(enum.Enum):
    buy = "buy"
    sell = "sell"


class Transaction(Base, TimestampMixin):
    __tablename__ = "transactions"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    bond_id = Column(BigInteger, ForeignKey("bonds.id"))
    user_id = Column(BigInteger, ForeignKey("users.id"))
    user = relationship("User", back_populates="transactions")
    transaction_type = Column(Enum(TransactionType))
