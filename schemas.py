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

class RentalAgreement(BaseModel):
    tool_code: str
    tool_type: str
    tool_brand: str
    rental_day_count: int
    checkout_date: date
    due_date: date
    daily_rental_charge: float
    charge_days: int
    pre_discount_charge: float
    discount_percent: int
    discount_amount: float
    final_charge: float

