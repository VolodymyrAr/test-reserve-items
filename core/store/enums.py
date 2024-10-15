import enum


class OrderStatus(enum.Enum):
    RESERVED = "RESERVED"
    SOLD = "SOLD"
    CANCELLED = "CANCELLED"
