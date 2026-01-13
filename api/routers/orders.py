from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from models.order import Order

router = APIRouter()

@router.post("/")
def create_order(amount: float, db: Session = Depends(get_db)):
    order = Order(amount=amount)
    db.add(order)
    db.commit()
    db.refresh(order)
    return {
        "order_id": order.id,
        "amount": order.amount,
        "status": order.status
    }
