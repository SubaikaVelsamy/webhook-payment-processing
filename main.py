from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.background import BackgroundTasks
from sqlalchemy.orm import Session
from db.database import Base, engine
from db.session import get_db, SessionLocal
import models, schemas
from schemas.schemas import OrderCreate, OrderResponse, PaymentCreate, PaymentResponse, WebhookEventCreate, WebhookEventResponse

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Webhook Payment Project")

@app.post("/orders/", response_model=OrderResponse)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    db_order = models.Order(user_id=order.user_id, amount=order.amount)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

@app.get("/orders/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

@app.post("/payments/", response_model=  PaymentResponse)
def create_payment(payment:   PaymentCreate, db: Session = Depends(get_db)):
    # Check if order exists
    db_order = db.query(models.Order).filter(models.Order.id == payment.order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Save payment
    db_payment = models.Payment(
        order_id=payment.order_id,
        provider_payment_id=payment.provider_payment_id,
        status=payment.status,
        raw_response=payment.raw_response
    )
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)

    # Update order status if payment successful
    if payment.status.lower() == "paid":
        db_order.status = "shipped"  # or "completed"
        db.commit()
        db.refresh(db_order)

    return db_payment


# ---------------- Webhook ----------------
@app.post("/webhook/")
async def webhook_listener(request: Request, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    payload = await request.json()
    event_id = payload.get("id")
    event_type = payload.get("type")

    # Avoid duplicate processing
    if db.query(models.WebhookEvent).filter(models.WebhookEvent.event_id == event_id).first():
        return {"message": "Event already processed"}

    # Save webhook event
    db_event = models.WebhookEvent(
        event_id=event_id,
        event_type=event_type,
        payload=payload
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)

    # Process event asynchronously
    background_tasks.add_task(process_webhook, db_event.id)

    return {"message": "Webhook received"}


# ---------------- Webhook Processor ----------------
def process_webhook(event_id: int):
    db = SessionLocal()  # independent session
    try:
        db_event = db.query(models.WebhookEvent).filter(models.WebhookEvent.id == event_id).first()
        if not db_event or db_event.processed:
            return

        # Example: Update order based on event payload
        order_id = db_event.payload.get("order_id")
        payment_status = db_event.payload.get("status")

        order = db.query(models.Order).filter(models.Order.id == order_id).first()
        if order:
            order.status = payment_status
            db.commit()

        db_event.processed = True
        db.commit()
    finally:
        db.close()
