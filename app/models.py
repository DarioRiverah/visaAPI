from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime
from typing import Optional, Dict

class CardType(str, Enum):
    classic = "Classic"
    gold = "Gold"
    platinum = "Platinum"
    black = "Black"
    white = "White"

class ClientIn(BaseModel):
    name: str = Field(..., min_length=1)
    country: str
    monthlyIncome: float = Field(..., ge=0)
    viseClub: bool
    cardType: CardType

class ClientOut(BaseModel):
    clientId: int
    name: str
    cardType: CardType
    status: str
    message: str

class ErrorOut(BaseModel):
    status: str = "Rejected"
    error: str

class PurchaseIn(BaseModel):
    clientId: int
    amount: float = Field(..., gt=0)
    currency: str
    purchaseDate: datetime
    purchaseCountry: str

class PurchaseApproved(BaseModel):
    status: str = "Approved"
    purchase: dict

class PurchaseRejected(BaseModel):
    status: str = "Rejected"
    error: str
