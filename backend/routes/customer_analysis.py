# """
# Customer analytics routes.
# Each endpoint calls analytics functions and returns JSON.
# """

# from typing import List

# from fastapi import APIRouter, Query

# from .. import analytics, schemas


# router = APIRouter(prefix="/analytics/customers", tags=["customers"])


# @router.get("/top-spenders", response_model=List[schemas.TopCustomerBySpending])
# def top_customers_by_spending(limit: int = Query(10, ge=1, le=100)):
#     """
#     Top N customers by total spending.
#     """
#     return analytics.top_customers_by_spending(limit)


# @router.get("/top-by-orders", response_model=List[schemas.TopCustomerByOrders])
# def top_customers_by_orders(limit: int = Query(10, ge=1, le=100)):
#     """
#     Top N customers by number of orders.
#     """
#     return analytics.top_customers_by_orders(limit)


# @router.get("/by-city", response_model=List[schemas.CustomersByCity])
# def customers_by_city():
#     """
#     Number of customers from each city.
#     """
#     return analytics.customers_by_city()


"""Customer analytics routes."""

from typing import List
from fastapi import APIRouter, Query
from .. import analytics, schemas

router = APIRouter(prefix="/analytics/customers", tags=["customers"])

@router.get("/top-spenders", response_model=List[schemas.TopCustomerBySpending])
def top_customers_by_spending(limit: int = Query(10, ge=1, le=100)):
    return analytics.top_customers_by_spending(limit)

@router.get("/top-by-orders", response_model=List[schemas.TopCustomerByOrders])
def top_customers_by_orders(limit: int = Query(10, ge=1, le=100)):
    return analytics.top_customers_by_orders(limit)

@router.get("/by-city", response_model=List[schemas.CustomersByCity])
def customers_by_city():
    return analytics.customers_by_city()

@router.get("/lifetime-value", response_model=List[schemas.CustomerLifetimeValue])
def customer_lifetime_value(limit: int = Query(20, ge=1, le=100)):
    """Customer Lifetime Value: spend, frequency, lifespan."""
    return analytics.customer_lifetime_value(limit)

@router.get("/repeat-vs-new", response_model=List[schemas.RepeatVsNew])
def repeat_vs_new_customers():
    """Repeat customers vs one-time buyers."""
    return analytics.repeat_vs_new_customers()

@router.get("/order-frequency", response_model=List[schemas.CustomerOrderFrequency])
def customer_order_frequency():
    """Distribution of order counts per customer."""
    return analytics.customer_order_frequency()
