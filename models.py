from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import datetime
from fastapi import FastAPI
from enum import Enum

# orderStatus Enum to represent the status of an order
class OrderStatus(str, Enum):
    PREPARING = "preparing"
    PICKED_UP = "picked_up"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"

# database model for the Order table
from datetime import datetime, timezone
from typing import Optional
from sqlmodel import SQLModel, Field

class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_name: str
    delivery_address: str
    items: str
    status: OrderStatus = Field(default=OrderStatus.PREPARING)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# schema for creating a new order
class OrderCreate(SQLModel):
    customer_name: str
    delivery_address: str
    items: str

# schema for updating an existing order's status

class OrderUpdate(SQLModel):
    status: Optional[OrderStatus] = None
    delivery_address: Optional[str] = None

# statuslog model to keep track of the status changes of an order

class StatusLog(SQLModel):
    order_id: int
    old_status: str
    new_status: str
    changed_at: datetime
