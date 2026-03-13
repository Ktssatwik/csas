# """
# Order analytics routes.
# Each endpoint calls analytics functions and returns JSON.
# """

# from fastapi import APIRouter

# from .. import analytics, schemas


# router = APIRouter(prefix="/analytics/orders", tags=["orders"])


# @router.get("/average-order-value", response_model=schemas.AverageOrderValue)
# def average_order_value():
#     """
#     Average order value.
#     """
#     return analytics.average_order_value()


# @router.get("/average-items-per-order", response_model=schemas.AverageItemsPerOrder)
# def average_items_per_order():
#     """
#     Average items per order.
#     """
#     return analytics.average_items_per_order()


"""Order analytics routes."""

from typing import List
from fastapi import APIRouter, Query
from .. import analytics, schemas

router = APIRouter(prefix="/analytics/orders", tags=["orders"])

@router.get("/average-order-value", response_model=schemas.AverageOrderValue)
def average_order_value():
    return analytics.average_order_value()

@router.get("/average-items-per-order", response_model=schemas.AverageItemsPerOrder)
def average_items_per_order():
    return analytics.average_items_per_order()

@router.get("/value-distribution", response_model=List[schemas.OrderValueDistribution])
def order_value_distribution():
    """Orders bucketed into spend tiers."""
    return analytics.order_value_distribution()

@router.get("/high-value", response_model=List[schemas.HighValueOrder])
def high_value_orders(limit: int = Query(10, ge=1, le=100)):
    """Top N highest-value individual orders."""
    return analytics.high_value_orders(limit)
