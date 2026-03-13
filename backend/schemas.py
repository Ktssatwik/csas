
# """
# Pydantic response models for analytics endpoints.
# These models define the JSON shape returned by the API.
# """

# from pydantic import BaseModel


# # ----------------------------
# # Customer Analytics Schemas
# # ----------------------------


# class TopCustomerBySpending(BaseModel):
#     customer_id: int
#     name: str
#     city: str
#     total_spend: float
#     total_orders: int


# class TopCustomerByOrders(BaseModel):
#     customer_id: int
#     name: str
#     city: str
#     orders_count: int


# class CustomersByCity(BaseModel):
#     city: str
#     customer_count: int


# # ----------------------------
# # Product Analytics Schemas
# # ----------------------------


# class TopProductByRevenue(BaseModel):
#     product_id: int
#     product_name: str
#     category: str
#     total_revenue: float


# class TopProductByQuantity(BaseModel):
#     product_id: int
#     product_name: str
#     category: str
#     total_quantity: int


# class ItemsSoldPerCategory(BaseModel):
#     category: str
#     total_quantity: int


# class RevenueByCategory(BaseModel):
#     category: str
#     total_revenue: float


# class UnderperformingProduct(BaseModel):
#     product_id: int
#     product_name: str
#     category: str
#     total_revenue: float


# # ----------------------------
# # Sales Analytics Schemas
# # ----------------------------


# class MonthlySalesTrend(BaseModel):
#     month: str
#     total_revenue: float


# class OrdersPerMonth(BaseModel):
#     month: str
#     orders_count: int


# class RevenueByCity(BaseModel):
#     city: str
#     total_revenue: float


# class OrderStatusBreakdown(BaseModel):
#     status: str
#     orders_count: int
#     percentage_of_total: float


# # ----------------------------
# # Order Analytics Schemas
# # ----------------------------


# class AverageOrderValue(BaseModel):
#     avg_order_value: float


# class AverageItemsPerOrder(BaseModel):
#     avg_items_per_order: float


"""
Pydantic response models for all analytics endpoints.
"""

from typing import Optional
from datetime import date

from pydantic import BaseModel


# ----------------------------
# Customer Analytics
# ----------------------------

class TopCustomerBySpending(BaseModel):
    customer_id: int
    name: str
    city: str
    total_spend: float
    total_orders: int

class TopCustomerByOrders(BaseModel):
    customer_id: int
    name: str
    city: str
    orders_count: int

class CustomersByCity(BaseModel):
    city: str
    customer_count: int

class CustomerLifetimeValue(BaseModel):
    customer_id: int
    name: str
    city: str
    total_orders: int
    total_spend: float
    avg_order_value: float
    customer_lifespan_days: Optional[int]

class RepeatVsNew(BaseModel):
    customer_type: str
    customer_count: int

class CustomerOrderFrequency(BaseModel):
    order_count: int
    num_customers: int


# ----------------------------
# Product Analytics
# ----------------------------

class TopProductByRevenue(BaseModel):
    product_id: int
    product_name: str
    category: str
    total_revenue: float

class TopProductByQuantity(BaseModel):
    product_id: int
    product_name: str
    category: str
    total_quantity: int

class ItemsSoldPerCategory(BaseModel):
    category: str
    total_quantity: int

class RevenueByCategory(BaseModel):
    category: str
    total_revenue: float

class UnderperformingProduct(BaseModel):
    product_id: int
    product_name: str
    category: str
    total_revenue: float

class ProductPriceVsRevenue(BaseModel):
    product_name: str
    category: str
    price: float
    total_units_sold: int
    total_revenue: float

class CategoryAvgPrice(BaseModel):
    category: str
    avg_price: float
    product_count: int


# ----------------------------
# Sales Analytics
# ----------------------------

class MonthlySalesTrend(BaseModel):
    month: str
    total_revenue: float

class OrdersPerMonth(BaseModel):
    month: str
    orders_count: int

class RevenueByCity(BaseModel):
    city: str
    total_revenue: float

class OrderStatusBreakdown(BaseModel):
    status: str
    orders_count: int
    percentage_of_total: float

class MonthlyRevenueGrowth(BaseModel):
    month: str
    total_revenue: float
    prev_revenue: Optional[float]
    growth_pct: Optional[float]

class RevenueByWeekday(BaseModel):
    weekday: str
    day_num: int
    total_revenue: float
    orders_count: int

class CityCategoryCombo(BaseModel):
    city: str
    category: str
    total_revenue: float


# ----------------------------
# Order Analytics
# ----------------------------

class AverageOrderValue(BaseModel):
    avg_order_value: float

class AverageItemsPerOrder(BaseModel):
    avg_items_per_order: float

class OrderValueDistribution(BaseModel):
    value_bucket: str
    orders_count: int

class HighValueOrder(BaseModel):
    order_id: int
    customer_name: str
    city: str
    order_date: date
    status: str
    order_total: float
    distinct_products: int
