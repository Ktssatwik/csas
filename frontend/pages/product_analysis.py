# """
# Product analytics page.
# Calls FastAPI endpoints and renders charts.
# """

# import os

# import pandas as pd
# import plotly.express as px
# import requests
# import streamlit as st
# from dotenv import load_dotenv


# # Load API base URL from .env
# load_dotenv()
# API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")


# def get_data(path: str):
#     """
#     Call API and return JSON.
#     """
#     url = f"{API_BASE_URL}{path}"
#     response = requests.get(url, timeout=30)
#     response.raise_for_status()
#     return response.json()


# st.title("Product Analysis")


# st.subheader("Top Products by Revenue")
# data = get_data("/analytics/products/top-by-revenue?limit=10")
# df = pd.DataFrame(data)
# if not df.empty:
#     fig = px.bar(df, x="product_name", y="total_revenue", color="category")
#     st.plotly_chart(fig, use_container_width=True)
#     st.dataframe(df, use_container_width=True)


# st.subheader("Top Products by Quantity Sold")
# data = get_data("/analytics/products/top-by-quantity?limit=10")
# df = pd.DataFrame(data)
# if not df.empty:
#     fig = px.bar(df, x="product_name", y="total_quantity", color="category")
#     st.plotly_chart(fig, use_container_width=True)
#     st.dataframe(df, use_container_width=True)


# st.subheader("Items Sold per Category")
# data = get_data("/analytics/products/items-per-category")
# df = pd.DataFrame(data)
# if not df.empty:
#     fig = px.bar(df, x="category", y="total_quantity", title="Items Sold per Category" , color="category")
#     st.plotly_chart(fig, use_container_width=True)
#     st.dataframe(df, use_container_width=True)


# st.subheader("Revenue by Category")
# data = get_data("/analytics/products/revenue-by-category")
# df = pd.DataFrame(data)
# if not df.empty:
#     fig = px.bar(df, x="category", y="total_revenue", title="Revenue by Category", color="category")
#     st.plotly_chart(fig, use_container_width=True)
#     st.dataframe(df, use_container_width=True)


# st.subheader("Underperforming Products")
# data = get_data("/analytics/products/underperforming?limit=10")
# df = pd.DataFrame(data)
# if not df.empty:
#     fig = px.bar(df, x="product_name", y="total_revenue", color="category", title="Lowest Revenue Products")
#     st.plotly_chart(fig, use_container_width=True)
#     st.dataframe(df, use_container_width=True)


"""
CSAS — Product Analytics Page
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import sys

# Ensure this pages folder is on the path so _shared can be imported
sys.path.append(os.path.dirname(__file__))

from _shared import (  # noqa: E402
    apply_global_styles,
    page_header,
    section_header,
    insight,
    get_data,
    apply_chart_style,
    sidebar_nav,
    NEON_COLORS,
)

st.set_page_config(page_title="CSAS // Products", page_icon="◈", layout="wide")
apply_global_styles()
sidebar_nav()

page_header("PRODUCT ANALYTICS", "REVENUE · VOLUME · CATEGORY INTELLIGENCE", "#0099ff")

# ── KPIs ──────────────────────────────────────────────────────────────────────
section_header("PRODUCT OVERVIEW")

cat_rev  = get_data("/analytics/products/revenue-by-category")
cat_qty  = get_data("/analytics/products/items-per-category")
cat_price = get_data("/analytics/products/category-avg-price")

df_cat_rev   = pd.DataFrame(cat_rev)
df_cat_qty   = pd.DataFrame(cat_qty)
df_cat_price = pd.DataFrame(cat_price)

total_rev = df_cat_rev["total_revenue"].sum() if not df_cat_rev.empty else 0
top_cat   = df_cat_rev.iloc[0]["category"] if not df_cat_rev.empty else "—"
total_units = df_cat_qty["total_quantity"].sum() if not df_cat_qty.empty else 0
num_cats = len(df_cat_rev) if not df_cat_rev.empty else 0

k1, k2, k3, k4 = st.columns(4)
k1.metric("TOTAL PRODUCT REVENUE", f"${total_rev:,.0f}")
k2.metric("TOP CATEGORY", top_cat)
k3.metric("TOTAL UNITS SOLD", f"{total_units:,}")
k4.metric("CATEGORIES", num_cats)

st.markdown("<br>", unsafe_allow_html=True)

# ── CATEGORY OVERVIEW ─────────────────────────────────────────────────────────
section_header("CATEGORY PERFORMANCE")

col1, col2, col3 = st.columns(3)

with col1:
    if not df_cat_rev.empty:
        fig = px.pie(df_cat_rev, names="category", values="total_revenue",
                     title="REVENUE SHARE BY CATEGORY",
                     hole=0.5, color_discrete_sequence=NEON_COLORS)
        apply_chart_style(fig)
        st.plotly_chart(fig, use_container_width=True)

with col2:
    if not df_cat_qty.empty:
        fig = px.bar(df_cat_qty, x="category", y="total_quantity",
                     title="UNITS SOLD PER CATEGORY",
                     color="total_quantity",
                     color_continuous_scale=["#050810", "#0033ff", "#0099ff"],
                     labels={"category": "Category", "total_quantity": "Units"})
        apply_chart_style(fig)
        fig.update_coloraxes(showscale=False)
        fig.update_layout(xaxis_tickangle=-25)
        st.plotly_chart(fig, use_container_width=True)

with col3:
    if not df_cat_price.empty:
        fig = px.bar(df_cat_price, x="category", y="avg_price",
                     title="AVG PRICE BY CATEGORY",
                     color="avg_price",
                     color_continuous_scale=["#050810", "#cc00ff", "#ff007f"],
                     labels={"category": "Category", "avg_price": "Avg Price ($)"})
        apply_chart_style(fig)
        fig.update_coloraxes(showscale=False)
        fig.update_layout(xaxis_tickangle=-25)
        st.plotly_chart(fig, use_container_width=True)

if not df_cat_rev.empty:
    best = df_cat_rev.iloc[0]
    insight(f"'{best['category']}' leads all categories with ${best['total_revenue']:,.0f} in revenue — {best['total_revenue']/total_rev*100:.1f}% of total.")

# ── PRICE vs REVENUE SCATTER ──────────────────────────────────────────────────
section_header("PRICING INTELLIGENCE — SWEET SPOT ANALYSIS")

pvr_data = get_data("/analytics/products/price-vs-revenue")
df_pvr = pd.DataFrame(pvr_data)

if not df_pvr.empty:
    fig = px.scatter(df_pvr, x="price", y="total_revenue",
                     size="total_units_sold", color="category",
                     hover_name="product_name",
                     title="PRICE vs REVENUE vs UNITS SOLD",
                     labels={"price": "Unit Price ($)", "total_revenue": "Total Revenue ($)",
                             "total_units_sold": "Units Sold"},
                     color_discrete_sequence=NEON_COLORS)
    apply_chart_style(fig)
    fig.update_traces(marker=dict(line=dict(width=1, color="rgba(255,255,255,0.15)")))
    # Add a trend line
    fig.update_layout(height=480)
    st.plotly_chart(fig, use_container_width=True)
    insight("Bubble size = units sold. Large bubbles at lower price points are high-volume low-margin heroes; small bubbles at top-right are premium anchors.")

# ── TOP PRODUCTS ──────────────────────────────────────────────────────────────
section_header("TOP PRODUCTS")

limit = st.select_slider("Show top N products", options=[5,10,15,20,25], value=10, key="prod_limit")

col1, col2 = st.columns(2)

with col1:
    rev_data = get_data(f"/analytics/products/top-by-revenue?limit={limit}")
    df_rev = pd.DataFrame(rev_data)
    if not df_rev.empty:
        fig = px.bar(df_rev, x="total_revenue", y="product_name",
                     orientation="h", color="category",
                     title=f"TOP {limit} BY REVENUE",
                     labels={"product_name": "", "total_revenue": "Revenue ($)"},
                     color_discrete_sequence=NEON_COLORS)
        apply_chart_style(fig)
        fig.update_layout(height=400, yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig, use_container_width=True)

with col2:
    qty_data = get_data(f"/analytics/products/top-by-quantity?limit={limit}")
    df_qty = pd.DataFrame(qty_data)
    if not df_qty.empty:
        fig = px.bar(df_qty, x="total_quantity", y="product_name",
                     orientation="h", color="category",
                     title=f"TOP {limit} BY UNITS SOLD",
                     labels={"product_name": "", "total_quantity": "Units"},
                     color_discrete_sequence=NEON_COLORS)
        apply_chart_style(fig)
        fig.update_layout(height=400, yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig, use_container_width=True)

# ── UNDERPERFORMING ───────────────────────────────────────────────────────────
section_header("UNDERPERFORMING PRODUCTS — LOWEST REVENUE")

under_data = get_data(f"/analytics/products/underperforming?limit={limit}")
df_under = pd.DataFrame(under_data)
if not df_under.empty:
    fig = px.bar(df_under, x="product_name", y="total_revenue",
                 color="category",
                 title=f"BOTTOM {limit} PRODUCTS BY REVENUE",
                 labels={"product_name": "Product", "total_revenue": "Revenue ($)"},
                 color_discrete_sequence=["#ff4060", "#ff8c00", "#ffb400",
                                          "#cc00ff", "#0099ff"])
    apply_chart_style(fig)
    fig.update_layout(xaxis_tickangle=-30)
    st.plotly_chart(fig, use_container_width=True)
    insight(f"These {limit} products generate the least revenue. Consider promotions, bundling, or discontinuation review.")
    st.dataframe(df_under.style.format({"total_revenue": "${:,.2f}"}),
                 use_container_width=True, hide_index=True)
