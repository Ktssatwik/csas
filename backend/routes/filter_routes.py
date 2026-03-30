"""Simple filter routes for CSAS."""

from datetime import date
from typing import Optional

from fastapi import APIRouter, Query

from .. import filter_analysis

router = APIRouter(prefix="/analytics/filters", tags=["filters"])


@router.get("/customers/list")
def customers_list(
    city: Optional[str] = Query(None, description="Filter by customer city."),
    signup_from: Optional[date] = Query(None, description="Signup date start (YYYY-MM-DD)."),
    signup_to: Optional[date] = Query(None, description="Signup date end (YYYY-MM-DD)."),
    name_like: Optional[str] = Query(None, description="Search part of customer name."),
    min_orders: Optional[int] = Query(None, ge=0, description="Minimum order count."),
    top_n: int = Query(20, ge=1, le=200, description="Max rows to return."),
):
    """
    List customers with simple filters.
    """
    return filter_analysis.customers_list(
        city=city,
        signup_from=signup_from,
        signup_to=signup_to,
        name_like=name_like,
        min_orders=min_orders,
        top_n=top_n,
    )


@router.get("/customers/spend-summary")
def customers_spend_summary(
    city: Optional[str] = Query(None, description="Filter by customer city."),
    signup_from: Optional[date] = Query(None, description="Signup date start."),
    signup_to: Optional[date] = Query(None, description="Signup date end."),
    min_total_spend: Optional[float] = Query(None, ge=0, description="Minimum total spend."),
    max_total_spend: Optional[float] = Query(None, ge=0, description="Maximum total spend."),
    top_n: int = Query(20, ge=1, le=200, description="Max customers returned."),
):
    """
    Customer spend metrics: total spend, avg order value, total orders.
    """
    return filter_analysis.customers_spend_summary(
        city=city,
        signup_from=signup_from,
        signup_to=signup_to,
        min_total_spend=min_total_spend,
        max_total_spend=max_total_spend,
        top_n=top_n,
    )


@router.get("/orders/list")
def orders_list(
    date_from: Optional[date] = Query(None, description="Order date start."),
    date_to: Optional[date] = Query(None, description="Order date end."),
    status: Optional[str] = Query(None, description="Order status value."),
    customer_id: Optional[int] = Query(None, description="Specific customer id."),
    city: Optional[str] = Query(None, description="Customer city."),
    top_n: int = Query(20, ge=1, le=500, description="Max orders returned."),
):
    """
    List orders with status/date/customer filters.
    """
    return filter_analysis.orders_list(
        date_from=date_from,
        date_to=date_to,
        status=status,
        customer_id=customer_id,
        city=city,
        top_n=top_n,
    )


@router.get("/orders/value-summary")
def orders_value_summary(
    date_from: Optional[date] = Query(None, description="Order date start."),
    date_to: Optional[date] = Query(None, description="Order date end."),
    status: Optional[str] = Query(None, description="Order status."),
    customer_id: Optional[int] = Query(None, description="Specific customer."),
    min_order_total: Optional[float] = Query(None, ge=0, description="Minimum order value."),
    max_order_total: Optional[float] = Query(None, ge=0, description="Maximum order value."),
):
    """
    Order totals and item counts per order.
    """
    return filter_analysis.orders_value_summary(
        date_from=date_from,
        date_to=date_to,
        status=status,
        customer_id=customer_id,
        min_order_total=min_order_total,
        max_order_total=max_order_total,
    )


@router.get("/order-items/list")
def order_items_list(
    order_id: Optional[int] = Query(None, description="Specific order id."),
    product_id: Optional[int] = Query(None, description="Specific product id."),
    category: Optional[str] = Query(None, description="Product category."),
    min_quantity: Optional[int] = Query(None, ge=0, description="Minimum line quantity."),
    max_quantity: Optional[int] = Query(None, ge=0, description="Maximum line quantity."),
    top_n: int = Query(30, ge=1, le=500, description="Max rows returned."),
):
    """
    Raw order-item rows with line totals.
    """
    return filter_analysis.order_items_list(
        order_id=order_id,
        product_id=product_id,
        category=category,
        min_quantity=min_quantity,
        max_quantity=max_quantity,
        top_n=top_n,
    )


@router.get("/order-items/grouped")
def order_items_grouped(
    category: Optional[str] = Query(None, description="Product category."),
    product_id: Optional[int] = Query(None, description="Specific product id."),
    date_from: Optional[date] = Query(None, description="Order date start."),
    date_to: Optional[date] = Query(None, description="Order date end."),
    min_units: Optional[int] = Query(None, ge=0, description="Minimum units sold."),
    top_n: int = Query(20, ge=1, le=200, description="Max products returned."),
):
    """
    Product-level rollup from order_items: units, revenue, order_count.
    """
    return filter_analysis.order_items_grouped(
        category=category,
        product_id=product_id,
        date_from=date_from,
        date_to=date_to,
        min_units=min_units,
        top_n=top_n,
    )


@router.get("/products/list")
def products_list(
    category: Optional[str] = Query(None, description="Product category."),
    min_price: Optional[float] = Query(None, ge=0, description="Minimum price."),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum price."),
    name_like: Optional[str] = Query(None, description="Search part of product name."),
    product_id: Optional[int] = Query(None, description="Specific product id."),
    top_n: int = Query(30, ge=1, le=300, description="Max products returned."),
):
    """
    Basic products list with category/price/name filters.
    """
    return filter_analysis.products_list(
        category=category,
        min_price=min_price,
        max_price=max_price,
        name_like=name_like,
        product_id=product_id,
        top_n=top_n,
    )


@router.get("/products/sales-summary")
def products_sales_summary(
    category: Optional[str] = Query(None, description="Product category."),
    date_from: Optional[date] = Query(None, description="Sales date start."),
    date_to: Optional[date] = Query(None, description="Sales date end."),
    min_revenue: Optional[float] = Query(None, ge=0, description="Minimum product revenue."),
    max_revenue: Optional[float] = Query(None, ge=0, description="Maximum product revenue."),
    top_n: int = Query(20, ge=1, le=200, description="Max products returned."),
):
    """
    Product sales metrics: units sold, total revenue, order count.
    """
    return filter_analysis.products_sales_summary(
        category=category,
        date_from=date_from,
        date_to=date_to,
        min_revenue=min_revenue,
        max_revenue=max_revenue,
        top_n=top_n,
    )

