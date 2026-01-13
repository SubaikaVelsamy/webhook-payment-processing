from pydantic import BaseModel
from typing import Optional

# ---------------- Orders ----------------
class OrderCreate(BaseModel):
    user_id: int
    amount: float

class OrderResponse(OrderCreate):
    id: int
    status: str

    class Config:
        orm_mode = True

# ---------------- Payments ----------------
class PaymentCreate(BaseModel):
    order_id: int
    provider_payment_id: str
    status: str
    raw_response: Optional[dict] = None

class PaymentResponse(PaymentCreate):
    id: int

    class Config:
        orm_mode = True

# ---------------- Webhook Events ----------------
class WebhookEventCreate(BaseModel):
    event_id: str
    event_type: str
    payload: dict

class WebhookEventResponse(WebhookEventCreate):
    id: int
    processed: bool

    class Config:
        orm_mode = True
