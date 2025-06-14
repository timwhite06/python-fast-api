from datetime import datetime
from enum import Enum
from typing import Optional
from fastapi import FastAPI, HTTPException, Request
import json
import uvicorn
import logging
import time

app = FastAPI()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load order data
with open('./orders.json') as json_file:
    data = json.load(json_file)

def valid_order_id(order_id: str) -> bool:
    try:
        # Convert the order ID from base-16 hexadecimal to an base-10 integer to validate its format
        int(order_id, 16)
        return True
    except ValueError:
        return False

# APIs

# Using middleware to LOG requests and responses
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Log the incoming request
    logger.info(f"Request: {request.method} {request.url}")
    
    response = await call_next(request)
    
    # Log the response
    process_time = time.time() - start_time
    logger.info(f"Response: {response.status_code} - {process_time:.3f}s")
    
    return response

@app.get("/api/orders")
def get_order_by_id(
    id: Optional[str] = None, # Optional for filtering by order ID
    currency: Optional[str] = None, # Optional for filtering by order ID
    shipped_to: Optional[str] = None, # Optional for filtering by shipping address
    cost: Optional[float] = None # Optional for filtering by cost
    )-> dict:

    # Dictionary for filters used
    filters_used = {}
    filtered_orders = data

    # Apply filters based on query parameters
    if not any([id, currency, shipped_to, cost is not None]):
        raise HTTPException(status_code=400, detail="At least one filter must be provided")
    if id:
        if not valid_order_id(id):
            raise HTTPException(status_code=400, detail="Invalid order ID format")
        filtered_orders = [order for order in filtered_orders if order['id'] == id]
        filters_used['id'] = id

    if currency:
        filtered_orders = [order for order in filtered_orders if order['currency'] == currency]
        filters_used['currency'] = currency

    if shipped_to:
        # Search through the values of the shipping_address
        filtered_orders = [
            order for order in filtered_orders
            if shipped_to in order["customer"]["shipping_address"].values()
        ]

        if not filtered_orders:
            raise HTTPException(status_code=404, detail="No orders found matching the shipping address")

        filters_used["shipped_to"] = shipped_to

    if cost is not None:
        try:
            filtered_orders = [
                order for order in filtered_orders
                if float(order["price"]) >= cost
            ]
            filters_used["cost"] = cost
        except (KeyError, ValueError):
            raise HTTPException(status_code=400, detail="Invalid or missing price field in order data")


    # Return the filtered results
    if not filtered_orders:
        raise HTTPException(status_code=404, detail="No orders found matching the criteria")
    
    return {
        "results": len(filtered_orders),
        "filters": filters_used,
        "orders": filtered_orders # Using set to ensure unique orders - removing any duplicates
    }

class SortOrder(str, Enum):
    ascend = "ascend"
    descend = "descend"

@app.get("/api/orders/sort")
def get_sorted_orders(sort: SortOrder) -> dict:
    """
    Get all orders sorted by creation time (created_at field).
    'sort' parameter must be either 'ascend' or 'descend'.
    """
    # Sort the orders by created_at timestamp
    try:
        sorted_orders = sorted(
            data,
            key=lambda order: datetime.fromisoformat(order["created_at"].replace('Z', '+00:00')),
            reverse=(sort == SortOrder.descend)
        )
    except (KeyError, ValueError) as e:
        logger.error(f"Error sorting orders: {str(e)}")
        raise HTTPException(status_code=500, detail="Error sorting orders by timestamp")
    
    return {
        "results": len(sorted_orders),
        "sort_order": sort,
        "orders": sorted_orders
    }

def main():
    # Run the FastAPI app using uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")

if __name__ == "__main__":
    main()
