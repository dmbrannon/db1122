from pydantic import BaseModel
from datetime import date

class Tool(BaseModel):
    code: str
    type: str
    brand: str

class Price(BaseModel):
    type: str
    daily_rental_charge: float
    weekday_charge: bool
    weekend_charge: bool
    holiday_charge: bool

class Transaction(BaseModel):
    tool_code: str
    rental_day_count: int
    discount_percent: int
    checkout_date: date