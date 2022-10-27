from typing import TYPE_CHECKING
from sqlalchemy import Column, Unicode, BigInteger, Boolean, String

from core.db import Base
from core.db.mixins import TimestampMixin
from sqlalchemy.orm import relationship


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    password = Column(Unicode(255), nullable=False)
    email = Column(Unicode(255), nullable=False, unique=True)
    nickname = Column(Unicode(255), nullable=False, unique=True)
    is_admin = Column(Boolean, default=False)
    full_name = Column(Unicode(255), index=True)
    is_active = Column(Boolean(), default=True)
    bonds = relationship("Bond", back_populates="owner")
