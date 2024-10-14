from sqlalchemy import Column, String, Integer, ForeignKey, Enum, func, DateTime
from sqlalchemy.orm import relationship

from core.db import Base
from core.store.enums import OrderStatus


class CategoryModel(Base):
    name = Column(String(255))
    parent_id = Column(Integer, ForeignKey("category.id"))

    children = relationship("CategoryModel", backref="parent", remote_side="CategoryModel.id")


class ItemModel(Base):
    name = Column(String(255))
    price = Column(Integer)
    category_id = Column(Integer, ForeignKey("category.id"))
    stock = Column(Integer, default=0, index=True)

    category = relationship("CategoryModel", backref="store")


class OrderModel(Base):
    status = Column(Enum(OrderStatus), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    reserved_at = Column(DateTime, nullable=True)
    confirmed_at = Column(DateTime, nullable=True)

    user = relationship("UserModel", backref="orders")


class OrderItemModel(Base):
    order_id = Column(Integer, ForeignKey("order.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("item.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    quantity = Column(Integer, nullable=False, index=True)
    price = Column(Integer, nullable=False)
    discount = Column(Integer, nullable=False)

    order = relationship("OrderModel", backref="order_items")
    item = relationship("ItemModel", backref="order_items")


class DiscountModel(Base):
    category_id = Column(Integer, ForeignKey("category.id"), nullable=False)
    value = Column(Integer, nullable=False)
    is_active = Column(Integer, nullable=False)

    category = relationship("CategoryModel", backref="discounts")
