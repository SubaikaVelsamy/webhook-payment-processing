from fastapi import APIRouter, Request, Header, HTTPException, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from models.order import Order, OrderStatus
import hmac
import hashlib

router = APIRouter()

WEBHOOK_SECRET = "whsec_abc123"
