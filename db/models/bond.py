import uuid
import enum
from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, Unicode, BigInteger, DECIMAL, Enum
from sqlalchemy.orm import relationship

from core.db import Base
from core.db.mixins import TimestampMixin

if TYPE_CHECKING:
    from .user import User  # noqa: F401
    from .transaction import Transaction  # noqa: F401

class BondStatus(enum.Enum):
  posted = "posted"
  sold = "sold"

class Bond(Base, TimestampMixin):
    __tablename__ = "bonds"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(Unicode(255), index=True)
    description = Column(Unicode(255), index=False, nullable=True)
    quantity = Column(Integer, nullable=False)
    price = Column(DECIMAL(13, 4), nullable=False)
    owner_id = Column(BigInteger, ForeignKey("users.id"))
    owner = relationship("User", back_populates="bonds")
    status = Column(Enum(BondStatus), nullable=False, default=BondStatus.posted)