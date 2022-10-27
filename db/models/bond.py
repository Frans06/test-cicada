import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, Unicode
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import UUID

from core.db import Base
from core.db.mixins import TimestampMixin

if TYPE_CHECKING:
    from .user import User  # noqa: F401
    from .transaction import Transaction  # noqa: F401


class Bond(Base, TimestampMixin):
    __tablename__ = "bonds"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(Unicode(255), index=True)
    description = Column(Unicode(255), index=False, nullable=True)
    quantity = Column(Integer, nullable=False)
    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="items")
    transactions = relationship("Transaction", back_populates="bonds")
