import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, Unicode, BigInteger, DECIMAL
from sqlalchemy.orm import relationship

from core.db import Base
from core.db.mixins import TimestampMixin

if TYPE_CHECKING:
    from .user import User  # noqa: F401
    from .transaction import Transaction  # noqa: F401


class Bond(Base, TimestampMixin):
    __tablename__ = "bonds"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(Unicode(255), index=True)
    description = Column(Unicode(255), index=False, nullable=True)
    quantity = Column(Integer, nullable=False)
    price = Column(DECIMAL(10, 4), nullable=False)
    owner_id = Column(BigInteger, ForeignKey("users.id"))
    owner = relationship("User", back_populates="bonds")
