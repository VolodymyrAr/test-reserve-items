import enum


class OrderStatus(enum.Enum):
    RESERVED = "RESERVED"
    CANCELLED = "CANCELLED"
    SOLD = "SOLD"
