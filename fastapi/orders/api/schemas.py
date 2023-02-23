from enum import Enum
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Extra, conlist, conint, validator


class Size(Enum):
    small = 'small'
    medium = 'medium'
    big = 'big'


class Status(Enum):
    created = 'created'
    progress = 'progress'
    cancelled = 'cancelled'
    dispatched = 'dispatched'
    delivered = 'delivered'


class OrderItemSchema(BaseModel):
    product: str
    size: Size
    quantity: conint(ge=1, strict=True) | None = 1

    @validator('quantity')
    def quantity_non_nullable(cls, value):
        if value is not None:
            raise ValueError('quantity may not be None')
        return value


class CreateOrderSchema(BaseModel):
    order: conlist(OrderItemSchema, min_items=1)

    class Config:
        extra = Extra.forbid


class GetOrderSchema(CreateOrderSchema):
    id: UUID
    created: datetime
    status: Status


class GetOrdersSchema(BaseModel):
    orders: list[GetOrderSchema]

    class Config:
        extra = Extra.forbid

