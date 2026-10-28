from fastapi import APIRouter, Depends, HTTPException, Query
from database import get_session
from sqlmodel import Session, select
from models import Order, OrderCreate, OrderUpdate, StatusLog, OrderStatus
from datetime import datetime
# Depends is used for dependency injection


router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", response_model=Order)
def create_order(order: OrderCreate, session: Session = Depends(get_session)):
    try:
        db_order = Order(**order.model_dump())
        session.add(db_order)
        session.commit()
        session.refresh(db_order)
        return db_order
    except Exception:
        session.rollback()
        raise

@router.get("/", response_model=list[Order])
def list_orders(
    status: OrderStatus | None = Query(default=None, description="Filter orders by order status"),
    created_date: str | None = Query(default=None, description="Filter orders by creation date (YYYY-MM-DD)"),
    skip: int = Query(0,ge=0),
    limit: int = Query(20, ge=1, le=100),
    session: Session = Depends(get_session)
):
    query = select(Order)
    if status:
        query = query.where(Order.status == status)
    if created_date:
        start = datetime.combine(created_date, datetime.min.time())
        end = datetime.combine(created_date, datetime.max.time())

    query = query.offset(skip).limit(limit)

    return session.exec(query).all()

@router.patch("/statusUpdate/{order_id}", response_model=Order)
def update_order_status(order_id: int, order_update: OrderUpdate, session: Session = Depends(get_session)):
    db_order = session.get(Order, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    for key, value in order_update.model_dump(exclude_unset=True).items():
        setattr(db_order, key, value)
    
    session.add(db_order)
    session.commit()
    session.refresh(db_order)
    return db_order