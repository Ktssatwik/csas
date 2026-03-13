# """
# Product analytics routes.
# Each endpoint calls analytics functions and returns JSON.
# """

# from typing import List

# from fastapi import APIRouter, Query

# from .. import analytics, schemas


# router = APIRouter(prefix="/analytics/products", tags=["products"])


# @router.get("/top-by-revenue", response_model=List[schemas.TopProductByRevenue])
# def top_products_by_revenue(limit: int = Query(10, ge=1, le=100)):
#     """
#     Top N products by revenue.
#     """
#     return analytics.top_products_by_revenue(limit)


# @router.get("/top-by-quantity", response_model=List[schemas.TopProductByQuantity])
# def top_products_by_quantity(limit: int = Query(10, ge=1, le=100)):
#     """
#     Top N products by items sold.
#     """
#     return analytics.top_products_by_quantity(limit)


# @router.get("/items-per-category", response_model=List[schemas.ItemsSoldPerCategory])
# def items_sold_per_category():
#     """
#     Items sold per category.
#     """
#     return analytics.items_sold_per_category()


# @router.get("/revenue-by-category", response_model=List[schemas.RevenueByCategory])
# def revenue_by_category():
#     """
#     Revenue by category.
#     """
#     return analytics.revenue_by_category()


# @router.get("/underperforming", response_model=List[schemas.UnderperformingProduct])
# def underperforming_products(limit: int = Query(10, ge=1, le=100)):
#     """
#     Underperforming products by lowest revenue.
#     """
#     return analytics.underperforming_products(limit)


"""Product analytics routes."""

from typing import List
from fastapi import APIRouter, Query
from .. import analytics, schemas

router = APIRouter(prefix="/analytics/products", tags=["products"])

@router.get("/top-by-revenue", response_model=List[schemas.TopProductByRevenue])
def top_products_by_revenue(limit: int = Query(10, ge=1, le=100)):
    return analytics.top_products_by_revenue(limit)

@router.get("/top-by-quantity", response_model=List[schemas.TopProductByQuantity])
def top_products_by_quantity(limit: int = Query(10, ge=1, le=100)):
    return analytics.top_products_by_quantity(limit)

@router.get("/items-per-category", response_model=List[schemas.ItemsSoldPerCategory])
def items_sold_per_category():
    return analytics.items_sold_per_category()

@router.get("/revenue-by-category", response_model=List[schemas.RevenueByCategory])
def revenue_by_category():
    return analytics.revenue_by_category()

@router.get("/underperforming", response_model=List[schemas.UnderperformingProduct])
def underperforming_products(limit: int = Query(10, ge=1, le=100)):
    return analytics.underperforming_products(limit)

@router.get("/price-vs-revenue", response_model=List[schemas.ProductPriceVsRevenue])
def product_price_vs_revenue():
    """Price vs revenue scatter data — reveals pricing sweet spots."""
    return analytics.product_price_vs_revenue()

@router.get("/category-avg-price", response_model=List[schemas.CategoryAvgPrice])
def category_avg_price():
    """Average price and product count per category."""
    return analytics.category_avg_price()
