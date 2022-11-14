from fastapi import FastAPI, HTTPException
from schemas import Tool, Price, Transaction

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

@app.post("/transaction/", status_code=201, response_model=Transaction)
def create_transaction(*, transaction_in: Transaction) -> dict:
    """
    Create a new transaction (in memory only)
    """
    if transaction_in.rental_day_count < 1:
        raise HTTPException(
            status_code=422, detail=f"Rental day count must be an integer greater than zero"
        )

    if (transaction_in.discount_percent < -1) or (transaction_in.discount_percent > 100):
        raise HTTPException(
            status_code=422, detail=f"Transaction percent must be in range 0-100"
        )
    
    transaction_entry = Transaction(
        tool_code=transaction_in.tool_code,
        rental_day_count=transaction_in.rental_day_count,
        discount_percent=transaction_in.discount_percent,
        checkout_date=transaction_in.checkout_date
    )
    TRANSACTIONS.append(transaction_entry.dict())

    return transaction_entry
    