from sqlalchemy import Column, String, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship

from core.db import Base
from core.orders.enums import OrderStatus


class Category(Base):
    name = Column(String(255))
    parent_id = Column(Integer, ForeignKey("category.id"))

    children = relationship("Category", backref="parent", remote_side="category.id")


class Item(Base):
    name = Column(String(255))
    price = Column(String(255))
    category_id = Column(Integer, ForeignKey("category.id"))
    stock = Column(Integer, default=0, index=True)

    category = relationship("Category", backref="orders")


class Order(Base):
    status = Column(Enum(OrderStatus), nullable=False)


class OrderItem(Base):
    order_id = Column(Integer, ForeignKey("order.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("item.id"), nullable=False)
    quantity = Column(Integer, nullable=False, index=True)

    order = relationship("Order", backref="orders")


class Discount(Base):
    category_id = Column(Integer, ForeignKey("category.id"), nullable=False)
    value = Column(Integer, nullable=False)
    is_active = Column(Integer, nullable=False)

    category = relationship("Category", backref="discounts")
