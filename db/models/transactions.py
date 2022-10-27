import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import UUID

from core.db import Base
from core.db.mixins import TimestampMixin

if TYPE_CHECKING:
    from .bond import Bond  # noqa: F401


class Transaction(Base, TimestampMixin):
    __tablename__ = "transactions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    bond_id = Column(UUID, ForeignKey("bond.id"))
    bonds = relationship("Bond", back_populates="transactions")
