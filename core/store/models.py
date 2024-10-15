from sqlalchemy import Column, String, Integer, ForeignKey, Enum, func, DateTime, Boolean
from sqlalchemy.orm import relationship

from core.db import Base
from core.store.enums import OrderStatus


class Category(Base):
    name = Column(String(255))
    parent_id = Column(Integer, ForeignKey("category.id"))


class Item(Base):
    name = Column(String(255))
    price = Column(Integer)
    category_id = Column(Integer, ForeignKey("category.id"))
    stock = Column(Integer, default=0, index=True)

    category = relationship("Category", backref="store", lazy="joined")


class Order(Base):
    status = Column(Enum(OrderStatus), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    reserved_at = Column(DateTime, nullable=True)
    confirmed_at = Column(DateTime, nullable=True)

    user = relationship("User", backref="orders", lazy="joined")


class OrderItem(Base):
    order_id = Column(Integer, ForeignKey("order.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("item.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    quantity = Column(Integer, nullable=False, index=True)
    price = Column(Integer, nullable=False)
    discount = Column(Integer, nullable=False)

    order = relationship("Order", backref="order_items", lazy="joined")
    item = relationship("Item", backref="order_items", lazy="joined")


class Discount(Base):
    category_id = Column(Integer, ForeignKey("category.id"), nullable=False)
    value = Column(Integer, nullable=False)
    is_active = Column(Boolean, nullable=False)

    category = relationship("Category", backref="discounts", lazy="joined")
