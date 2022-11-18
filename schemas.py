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
    checkout_date: str # not date because of incoming format

class RentalAgreement(BaseModel):
    tool_code: str
    tool_type: str
    tool_brand: str
    rental_day_count: int
    checkout_date: str # not date because of incoming format
    due_date: str # not date because of incoming format
    daily_rental_charge: str # not float because of desired format
    charge_days: int
    pre_discount_charge: str # not float because of desired format
    discount_percent: str # not int because of desired format
    discount_amount: str # not float because of desired format
    final_charge: str # not float because of desired format

