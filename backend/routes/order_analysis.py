
"""Order analytics routes."""

from typing import List
from fastapi import APIRouter, Query
from .. import analytics, schemas

router = APIRouter(prefix="/analytics/orders", tags=["orders"])

@router.get("/average-order-value", response_model=schemas.AverageOrderValue)
async def average_order_value():
    return analytics.average_order_value()

@router.get("/average-items-per-order", response_model=schemas.AverageItemsPerOrder)
async def average_items_per_order():
    return analytics.average_items_per_order()

@router.get("/value-distribution", response_model=List[schemas.OrderValueDistribution])
async def order_value_distribution():
    """Orders bucketed into spend tiers."""
    return analytics.order_value_distribution()

@router.get("/high-value", response_model=List[schemas.HighValueOrder])
async def high_value_orders(limit: int = Query(10, ge=1, le=100)):
    """Top N highest-value individual orders."""
    return analytics.high_value_orders(limit)



# What is the difference between response_model and Depends(...)?
# If an endpoint only reads data, which method is preferred: GET or POST? Why?
# In your project, where does DB data get converted to JSON for browser response?
# Why does cursor.fetchone() in your crud.py return a dict and not a tuple?
# When does CORS error appear, and when does it not?
# If you remove CORS middleware and Streamlit still works, what is the likely reason?
# What is DI in one line?
# Is SQLAlchemy always async? If not, what makes it async?
# Can GET technically run INSERT? Should we do it?
# Why are your Pydantic schema classes useful in this project?