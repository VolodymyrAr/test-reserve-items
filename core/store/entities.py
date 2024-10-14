from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from core.entities import Entity
from core.store.enums import OrderStatus


class Category(Entity):
    id: int
    name: str
    children: Optional[List["Category"]] = []


class ItemBase(Entity):
    price: Decimal
    discount: Decimal

    @property
    def actual_price(self) -> Decimal:
        return Decimal(self.price * ((100 - self.discount) / 100))


class Item(ItemBase):
    id: int
    name: str
    stock: int
    category: str


class OrderItem(ItemBase):
    name: int
    quantity: int


class Order(Entity):
    id: str
    item: OrderItem
    status: OrderStatus

    @property
    def amount(self) -> Decimal:
        amount = self.item.quantity * self.price
        return amount


class ItemReport(ItemBase):
    id: int
    name: str
    quantity: int
    reserved_at: datetime
    ordered_at: datetime
