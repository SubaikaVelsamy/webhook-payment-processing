# Webhook-Driven Order & Payment Processing Backend

## 📌 Project Description
This project is a backend system that simulates a real-world payment processing workflow using webhook-based event handling.  
It demonstrates how modern backend systems handle orders, payments, asynchronous processing, retries, and idempotency.

The system is designed similar to real payment gateways like Stripe or Razorpay, where payment status updates are received via webhooks.

---

## 🛠️ Tech Stack
- Python 3.10+
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- JWT Authentication
- Celery
- Redis
- Docker & Docker Compose
- Pytest

---

## 🔄 High-Level Flow
1. User creates an order
2. Backend generates a payment intent
3. Payment gateway (mock service) processes payment
4. Payment gateway sends webhook event
5. Backend validates webhook signature
6. Webhook event is processed asynchronously
7. Order status is updated
8. Notification/background tasks are triggered

---

## 🎯 Key Concepts Demonstrated
- Webhook handling
- Idempotency
- Background job processing
- Retry mechanisms
- Secure API design
- Event-driven architecture
