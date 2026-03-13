# """
# Sales analytics routes.
# Each endpoint calls analytics functions and returns JSON.
# """

# from typing import List

# from fastapi import APIRouter

# from .. import analytics, schemas


# router = APIRouter(prefix="/analytics/sales", tags=["sales"])


# @router.get("/monthly-trend", response_model=List[schemas.MonthlySalesTrend])
# def monthly_sales_trend():
#     """
#     Monthly sales trend by revenue.
#     """
#     return analytics.monthly_sales_trend()


# @router.get("/orders-per-month", response_model=List[schemas.OrdersPerMonth])
# def orders_per_month():
#     """
#     Number of orders per month.
#     """
#     return analytics.orders_per_month()


# @router.get("/revenue-by-city", response_model=List[schemas.RevenueByCity])
# def revenue_by_city():
#     """
#     Revenue by customer city.
#     """
#     return analytics.revenue_by_city()


# @router.get("/status-breakdown", response_model=List[schemas.OrderStatusBreakdown])
# def order_status_breakdown():
#     """
#     Order status breakdown.
#     """
#     return analytics.order_status_breakdown()


"""Sales analytics routes."""

from typing import List
from fastapi import APIRouter
from .. import analytics, schemas

router = APIRouter(prefix="/analytics/sales", tags=["sales"])

@router.get("/monthly-trend", response_model=List[schemas.MonthlySalesTrend])
def monthly_sales_trend():
    return analytics.monthly_sales_trend()

@router.get("/orders-per-month", response_model=List[schemas.OrdersPerMonth])
def orders_per_month():
    return analytics.orders_per_month()

@router.get("/revenue-by-city", response_model=List[schemas.RevenueByCity])
def revenue_by_city():
    return analytics.revenue_by_city()

@router.get("/status-breakdown", response_model=List[schemas.OrderStatusBreakdown])
def order_status_breakdown():
    return analytics.order_status_breakdown()

@router.get("/monthly-growth", response_model=List[schemas.MonthlyRevenueGrowth])
def monthly_revenue_growth():
    """Month-over-month revenue growth percentage."""
    return analytics.monthly_revenue_growth()

@router.get("/revenue-by-weekday", response_model=List[schemas.RevenueByWeekday])
def revenue_by_weekday():
    """Revenue and order count by day of week."""
    return analytics.revenue_by_weekday()

@router.get("/city-category-heatmap", response_model=List[schemas.CityCategoryCombo])
def top_city_category_combos():
    """City × category revenue heatmap data."""
    return analytics.top_city_category_combos()