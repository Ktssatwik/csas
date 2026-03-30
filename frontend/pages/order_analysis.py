"""
CSAS — Order Analytics Page
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import sys

# Ensure this pages folder is on the path so _shared can be imported
sys.path.append(os.path.dirname(__file__))

from _shared import (  
    apply_global_styles,
    page_header,
    section_header,
    insight,
    get_data,
    apply_chart_style,
    sidebar_nav,
    NEON_COLORS,
)

st.set_page_config(page_title="CSAS // Orders", page_icon="◈", layout="wide")
apply_global_styles()
sidebar_nav()

page_header("ORDER ANALYTICS", "VALUE · DISTRIBUTION · HIGH-VALUE DEEP DIVE", "#ffb400")

# ── KPIs ──────────────────────────────────────────────────────────────────────
section_header("ORDER METRICS")

avg_val  = get_data("/analytics/orders/average-order-value")
avg_items = get_data("/analytics/orders/average-items-per-order")
dist_data = get_data("/analytics/orders/value-distribution")
hv_data   = get_data("/analytics/orders/high-value")

df_dist = pd.DataFrame(dist_data)
df_hv   = pd.DataFrame(hv_data)

total_orders = df_dist["orders_count"].sum() if not df_dist.empty else 0
top_bucket   = df_dist.loc[df_dist["orders_count"].idxmax(), "value_bucket"] if not df_dist.empty else "—"
max_order    = df_hv.iloc[0]["order_total"] if not df_hv.empty else 0

k1, k2, k3, k4 = st.columns(4)
k1.metric("AVG ORDER VALUE", f"${avg_val.get('avg_order_value', '—')}" if avg_val else "—")
k2.metric("AVG ITEMS / ORDER", avg_items.get("avg_items_per_order", "—") if avg_items else "—")
k3.metric("MOST COMMON SPEND TIER", top_bucket)
k4.metric("HIGHEST SINGLE ORDER", f"${max_order:,.2f}" if max_order else "—")

st.markdown("<br>", unsafe_allow_html=True)

# ── VALUE DISTRIBUTION ────────────────────────────────────────────────────────
section_header("ORDER VALUE DISTRIBUTION")

BUCKET_ORDER = ["Under $50", "$50–$100", "$100–$200", "$200–$500", "Over $500"]

if not df_dist.empty:
    df_dist["value_bucket"] = pd.Categorical(df_dist["value_bucket"],
                                              categories=BUCKET_ORDER, ordered=True)
    df_dist = df_dist.sort_values("value_bucket")

    # col1, col2, col3 = st.columns(3)
    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(df_dist, x="value_bucket", y="orders_count",
                     title="ORDERS BY SPEND TIER",
                     color="orders_count",
                     color_continuous_scale=["#1DD144", "#7b2fff", "#ffb400"],
                     labels={"value_bucket": "Spend Tier", "orders_count": "Orders"})
        apply_chart_style(fig)
        fig.update_coloraxes(showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig2 = px.pie(df_dist, names="value_bucket", values="orders_count",
                      title="SPEND TIER SHARE", hole=0.5,
                      color_discrete_sequence=["#00ffc8", "#0099ff", "#cc00ff",
                                               "#ffb400", "#ff4060"],
                      category_orders={"value_bucket": BUCKET_ORDER})
        apply_chart_style(fig2)
        st.plotly_chart(fig2, use_container_width=True)
    
    # with col3:
    #     st.write("hye uys")

    top_tier = df_dist.loc[df_dist["orders_count"].idxmax()]
    pct = round(top_tier["orders_count"] / total_orders * 100, 1)
    insight(f"'{top_tier['value_bucket']}' is the most common order tier at {pct}% of all orders ({top_tier['orders_count']:,} orders).")

# ── HIGH VALUE ORDERS ─────────────────────────────────────────────────────────
section_header("HIGH-VALUE ORDERS — TOP 10")

limit_hv = st.select_slider("Show top N high-value orders", options=[5,10,15,20,25,50], value=10)
df_hv = pd.DataFrame(get_data(f"/analytics/orders/high-value?limit={limit_hv}"))

if not df_hv.empty:
    # Scatter by date
    fig = px.scatter(df_hv,
                     x="order_date", y="order_total",
                     size="distinct_products",
                     color="city",
                     hover_name="customer_name",
                     hover_data=["status", "distinct_products"],
                     title=f"TOP {limit_hv} HIGH-VALUE ORDERS OVER TIME",
                     labels={"order_date": "Order Date", "order_total": "Order Total ($)",
                             "distinct_products": "Products"},
                     color_discrete_sequence=NEON_COLORS)
    apply_chart_style(fig)
    fig.update_traces(marker=dict(line=dict(width=1, color="rgba(255,180,0,0.3)")))
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

    # Styled table
    st.dataframe(
        df_hv.rename(columns={
            "order_id": "Order ID", "customer_name": "Customer", "city": "City",
            "order_date": "Date", "status": "Status",
            "order_total": "Total ($)", "distinct_products": "Products"
        }).style.format({"Total ($)": "${:,.2f}"}),
        use_container_width=True, hide_index=True
    )

    # Status breakdown for high-value
    status_counts = df_hv["status"].value_counts().reset_index()
    status_counts.columns = ["status", "count"]
    fig2 = px.pie(status_counts, names="status", values="count",
                  title=f"STATUS BREAKDOWN — TOP {limit_hv} ORDERS",
                  hole=0.4,
                  color_discrete_sequence=["#00ffc8","#ff4060","#0099ff","#ffb400"])
    apply_chart_style(fig2)
    st.plotly_chart(fig2, use_container_width=True)

    insight(f"Top {limit_hv} orders average ${df_hv['order_total'].mean():,.2f} each. These accounts deserve white-glove retention treatment.")