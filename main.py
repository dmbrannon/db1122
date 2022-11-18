from fastapi import FastAPI, HTTPException
from schemas import Tool, Price, Transaction, RentalAgreement
from datetime import datetime, timedelta

TOOLS = [
    {
        "code": "CHNS",
        "type": "Chainsaw",
        "brand": "Stihl",
    },
    {
        "code": "LADW",
        "type": "Ladder",
        "brand": "Werner",
    },
    {
        "code": "JAKD",
        "type": "Jackhammer",
        "brand": "DeWalt",
    },
    {
        "code": "JAKR",
        "type": "Jackhammer",
        "brand": "Ridgid",
    },
]

PRICES = [
    {
        "type": "Ladder",
        "daily_rental_charge": 1.99,
        "weekday_charge": True,
        "weekend_charge": True,
        "holiday_charge": False, 
    },
    {
        "type": "Chainsaw",
        "daily_rental_charge": 1.49,
        "weekday_charge": True,
        "weekend_charge": False,
        "holiday_charge": True,
    },
    {
        "type": "Jackhammer",
        "daily_rental_charge": 2.99,
        "weekday_charge": True,
        "weekend_charge": False,
        "holiday_charge": False,
    },
    
]

TRANSACTIONS = []

app = FastAPI()
 

@app.get("/")
async def root():
    return {"message": TOOLS}

@app.get("/tool/{tool_code}", status_code=200)
def fetch_tool(*, tool_code: str) -> dict:
    """
    Fetch a single tool by its code
    """
    result = [tool for tool in TOOLS if tool["code"] == tool_code]
    if not result:
        raise HTTPException(
            status_code=404, detail=f"Tool with code {tool_code} not found"
        )

    return result[0]

@app.get("/price/{tool_type}", status_code=200)
def fetch_tool(*, tool_type: str) -> dict:
    """
    Fetch a single price by its type
    """
    result = [price for price in PRICES if price["type"] == tool_type]
    if not result:
        raise HTTPException(
            status_code=404, detail=f"Price with type {tool_type} not found"
        )

    return result[0]

@app.post("/tool/", status_code=201, response_model=Tool)
def create_tool(*, tool_in: Tool) -> dict:
    """
    Create a new tool (in memory only)
    """
    tool_entry = Tool(
        code=tool_in.code,
        type=tool_in.type,
        brand=tool_in.brand
    )
    TOOLS.append(tool_entry.dict())

    return tool_entry

@app.put("/price/{tool_type}", status_code=200, response_model=Price)
def update_price(*, tool_type: str, price_in: Price) -> dict:
    """
    Update an existing Price (in memory only)
    """
    tool_found = False
    for price in PRICES:
        if price["type"] == tool_type:
            price["daily_rental_charge"] = price_in.daily_rental_charge
            price["weekday_charge"] = price_in.weekday_charge
            price["weekend_charge"] = price_in.weekend_charge
            price["holiday_charge"] = price_in.holiday_charge
            tool_found = True

    if not tool_found:
        raise HTTPException(
            status_code=404, detail=f"Price with tool type {tool_type} not found"
        )
    return

@app.post("/transaction/", status_code=201, response_model=RentalAgreement)
def create_transaction(*, transaction_in: Transaction) -> dict:
    """
    Create a new transaction (in memory only)
    """
    if transaction_in.rental_day_count < 1:
        raise HTTPException(
            status_code=422, detail=f"Rental day count must be an integer greater than zero"
        )

    if (transaction_in.discount_percent < 0) or (transaction_in.discount_percent > 100):
        raise HTTPException(
            status_code=422, detail=f"Transaction percent must be in range 0-100"
        )

    try: 
        checkout_datetime = datetime.strptime(transaction_in.checkout_date, "%m/%d/%y")
    except:
        raise HTTPException(
            status_code=422, detail=f"Checkout date must be in format MM/DD/YY"
        )
    
    transaction_entry = Transaction(
        tool_code=transaction_in.tool_code,
        rental_day_count=transaction_in.rental_day_count,
        discount_percent=transaction_in.discount_percent,
        checkout_date=transaction_in.checkout_date
    )
    TRANSACTIONS.append(transaction_entry.dict())

    # Construct Rental Agreement
    for tool in TOOLS:
        if tool["code"] == transaction_in.tool_code:
            tool_type = tool["type"]
            tool_brand = tool["brand"]

    due_date_datetime = checkout_datetime + timedelta(days=transaction_in.rental_day_count)
    due_date = due_date_datetime.strftime("%m/%d/%y")
    for price in PRICES:
        if price["type"] == tool_type:
            daily_rental_charge = price["daily_rental_charge"]
            weekday_charge = price["weekday_charge"]
            weekend_charge = price["weekend_charge"]
            holiday_charge = price["holiday_charge"]

    datetimes_in_range = []
    for i in range(1, transaction_in.rental_day_count + 1):
        datetimes_in_range.append(checkout_datetime + timedelta(days=i))

    chargeable_days = [False] * transaction_in.rental_day_count
    for idx, date in enumerate(datetimes_in_range):
        # Calculate holidays charged
        ## Labor Day
        if holiday_charge and (date.month == 9) and (date.day < 7) and (date.weekday() == 0):
            chargeable_days[idx] = True
            continue
        elif not holiday_charge and ((date.month == 9) and (date.day < 7) and (date.weekday() == 0)):
            chargeable_days[idx] = False
            continue

        ## July 4th
        if (date.month == 7):
            fourth_of_july_datetime = datetime(date.year, 7, 4)
            if fourth_of_july_datetime.weekday() == 5: # Falls on a Saturday this year
                fourth_of_july_observed = datetime(date.year, 7, 3)
            elif fourth_of_july_datetime.weekday() == 6: # Falls on a Sunday this year
                fourth_of_july_observed = datetime(date.year, 7, 5)
            else: # Fourth of July is during the week
                fourth_of_july_observed = fourth_of_july_datetime
            
            if (fourth_of_july_observed.day == date.day) and holiday_charge:
                chargeable_days[idx] = True
                continue
            elif (fourth_of_july_observed.day == date.day) and not holiday_charge:
                chargeable_days[idx] = False
                continue

        # Calculate weekdays charged
        if (date.weekday() < 5) and (weekday_charge):
            chargeable_days[idx] = True

        # Calculate weekends charged
        if (date.weekday() > 4) and (weekend_charge):
            chargeable_days[idx] = True

    charge_days = chargeable_days.count(True)
    pre_discount_charge = round(charge_days * daily_rental_charge, 2)
    discount_amount = round((transaction_in.discount_percent / 100) * pre_discount_charge, 2)
    final_charge = pre_discount_charge - discount_amount

    rental_agreement = RentalAgreement(
        tool_code=transaction_in.tool_code,
        tool_type=tool_type,
        tool_brand=tool_brand,
        rental_day_count=transaction_in.rental_day_count,
        checkout_date=transaction_in.checkout_date,
        due_date=due_date,
        daily_rental_charge='${:,.2f}'.format(daily_rental_charge),
        charge_days=charge_days,
        pre_discount_charge='${:,.2f}'.format(pre_discount_charge),
        discount_percent=f'{transaction_in.discount_percent}%',
        discount_amount='${:,.2f}'.format(discount_amount),
        final_charge='${:,.2f}'.format(final_charge),
    )

    return rental_agreement

