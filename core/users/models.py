from sqlalchemy import Column, String, Boolean

from ..db import Base


class User(Base):
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, default=False)
