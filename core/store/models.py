from sqlalchemy import Column, String, Integer, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship

from core.db import Base
from core.store.enums import OrderStatus


class Category(Base):
    name = Column(String(255))
    parent_id = Column(Integer, ForeignKey("category.id"))


class Item(Base):
    name = Column(String(255))
    price = Column(Integer)
    category_id = Column(Integer, ForeignKey("category.id"), nullable=False)
    stock = Column(Integer, default=0, index=True)

    category = relationship("Category", backref="items", lazy="joined")


class Order(Base):
    status = Column(Enum(OrderStatus), nullable=False)
    item_id = Column(Integer, ForeignKey("item.id", ondelete="SET NULL"))
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    name = Column(String(255), nullable=False)
    quantity = Column(Integer, nullable=False, index=True)
    price = Column(Integer, nullable=False)
    discount = Column(Integer, nullable=True)

    user = relationship("User", backref="orders", lazy="joined")
    item = relationship("Item", backref="orders", lazy="joined")


class Discount(Base):
    category_id = Column(Integer, ForeignKey("category.id"), nullable=False)
    value = Column(Integer, nullable=False)
    is_active = Column(Boolean, nullable=False)

    category = relationship("Category", backref="discounts", lazy="joined")
