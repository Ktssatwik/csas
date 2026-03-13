# """
# Customer analytics page.
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


# st.title("Customer Analysis")


# # Top customers by spending
# st.subheader("Top Customers by Spending")
# data = get_data("/analytics/customers/top-spenders?limit=10")
# df = pd.DataFrame(data)
# if not df.empty:
#     fig = px.bar(df, x="name", y="total_spend", color="city", title="Top Spenders")
#     st.plotly_chart(fig, use_container_width=True)
#     st.dataframe(df, use_container_width=True)


# # Top customers by orders
# st.subheader("Top Customers by Orders")
# data = get_data("/analytics/customers/top-by-orders?limit=10")
# df = pd.DataFrame(data)
# if not df.empty:
#     fig = px.bar(df, x="name", y="orders_count", color="city", title="Most Frequent Customers")
#     st.plotly_chart(fig, use_container_width=True)
#     st.dataframe(df, use_container_width=True)


# # Customers by city
# st.subheader("Customers by City")
# data = get_data("/analytics/customers/by-city")
# df = pd.DataFrame(data)
# if not df.empty:
#     fig = px.pie(df, names="city", values="customer_count", title="Customer Distribution by City")
#     st.plotly_chart(fig, use_container_width=True)
#     st.dataframe(df, use_container_width=True)



"""
CSAS — Customer 
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

st.set_page_config(page_title="CSAS // Customers", page_icon="◈", layout="wide")
apply_global_styles()
sidebar_nav()

page_header("CUSTOMER ANALYTICS", "SPENDING · LOYALTY · GEOGRAPHY", "#00ffc8")
section_header("CUSTOMER ANALYSIS")

repeat_data = get_data("/analytics/customers/repeat-vs-new")
freq_data   = get_data("/analytics/customers/order-frequency")
clv_data    = get_data("/analytics/customers/lifetime-value?limit=20")

df_repeat = pd.DataFrame(repeat_data)
repeat_count = int(df_repeat.loc[df_repeat.customer_type == "Repeat", "customer_count"].values[0]) if not df_repeat.empty else 0
new_count    = int(df_repeat.loc[df_repeat.customer_type == "New",    "customer_count"].values[0]) if not df_repeat.empty else 0
total        = repeat_count + new_count
repeat_pct   = round(repeat_count / total * 100, 1) if total > 0 else 0

df_clv = pd.DataFrame(clv_data)
avg_clv    = round(df_clv["total_spend"].mean(), 2) if not df_clv.empty else 0
avg_lifespan = round(df_clv["customer_lifespan_days"].mean(), 0) if not df_clv.empty else 0

k1, k2, k3, k4 = st.columns(4)
k1.metric("TOTAL CUSTOMERS", f"{total:,}")
k2.metric("REPEAT RATE", f"{repeat_pct}%")
k3.metric("AVG LIFETIME VALUE", f"${avg_clv:,.2f}")
k4.metric("AVG CUSTOMER LIFESPAN", f"{avg_lifespan:.0f} days")

st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    # Donut: Repeat vs New
    if not df_repeat.empty:
        fig = go.Figure(go.Pie(
            labels=df_repeat["customer_type"],
            values=df_repeat["customer_count"],
            hole=0.65,
            marker=dict(colors=["#00ffc8", "#0099ff"],
                        line=dict(color="#050810", width=3)),
            textfont=dict(family="Share Tech Mono, monospace", size=12),
        ))
        fig.update_layout(title="REPEAT VS NEW CUSTOMERS",
                          annotations=[dict(text=f"{repeat_pct}%<br>repeat",
                                           font=dict(family="Orbitron,monospace",
                                                     size=16, color="#00ffc8"),
                                           showarrow=False)])
        apply_chart_style(fig)
        st.plotly_chart(fig, use_container_width=True)

with col2:
    # Bar: Order frequency distribution
    if freq_data:
        df_freq = pd.DataFrame(freq_data)
        fig = px.bar(df_freq, x="order_count", y="num_customers",
                     title="ORDER FREQUENCY DISTRIBUTION",
                     labels={"order_count": "Orders Placed", "num_customers": "Customers"},
                     color="num_customers",
                     color_continuous_scale=["#0033aa", "#00ffc8"])
        apply_chart_style(fig)
        fig.update_coloraxes(showscale=False)
        st.plotly_chart(fig, use_container_width=True)

insight(f"{repeat_pct}% of customers are repeat buyers — focus retention campaigns on the {new_count:,} one-time buyers to boost this ratio.")

# ── CLV TABLE ─────────────────────────────────────────────────────────────────
section_header("CUSTOMER LIFETIME VALUE — TOP 20")

if not df_clv.empty:
    # Scatter: CLV vs lifespan
    fig = px.scatter(df_clv, x="customer_lifespan_days", y="total_spend",
                     size="total_orders", color="city",
                     hover_name="name",
                     title="CLV MAP — SPEND vs LIFESPAN vs ORDER VOLUME",
                     labels={"customer_lifespan_days": "Lifespan (days)",
                             "total_spend": "Total Spend ($)",
                             "total_orders": "Orders"},
                     color_discrete_sequence=NEON_COLORS)
    apply_chart_style(fig)
    fig.update_traces(marker=dict(line=dict(width=1, color="rgba(0,255,200,0.3)")))
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(
        df_clv.rename(columns={
            "customer_id": "ID", "name": "Name", "city": "City",
            "total_orders": "Orders", "total_spend": "Total Spend ($)",
            "avg_order_value": "Avg Order ($)", "customer_lifespan_days": "Lifespan (days)"
        }).style.format({"Total Spend ($)": "${:,.2f}", "Avg Order ($)": "${:,.2f}"}),
        use_container_width=True, hide_index=True
    )

# ── TOP SPENDERS ──────────────────────────────────────────────────────────────
section_header("TOP SPENDERS")

limit = st.select_slider("Show top N customers", options=[5,10,15,20,25,50], value=10)
spend_data = get_data(f"/analytics/customers/top-spenders?limit={limit}")
df_spend = pd.DataFrame(spend_data)

if not df_spend.empty:
    col1, col2 = st.columns([2, 1])
    with col1:
        fig = px.bar(df_spend, x="name", y="total_spend",
                     color="city", title=f"TOP {limit} CUSTOMERS BY SPENDING",
                     labels={"name": "Customer", "total_spend": "Total Spend ($)"},
                     color_discrete_sequence=NEON_COLORS)
        apply_chart_style(fig)
        fig.update_layout(xaxis_tickangle=-35)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig2 = px.pie(df_spend, names="city", values="total_spend",
                      title="SPEND BY CITY",
                      color_discrete_sequence=NEON_COLORS,
                      hole=0.4)
        apply_chart_style(fig2)
        st.plotly_chart(fig2, use_container_width=True)

    st.dataframe(df_spend.style.format({"total_spend": "${:,.2f}"}),
                 use_container_width=True, hide_index=True)

# ── TOP BY ORDERS ─────────────────────────────────────────────────────────────
section_header("MOST FREQUENT CUSTOMERS")

ord_data = get_data(f"/analytics/customers/top-by-orders?limit={limit}")
df_ord = pd.DataFrame(ord_data)
if not df_ord.empty:
    fig = px.bar(df_ord, x="name", y="orders_count", color="city",
                 title=f"TOP {limit} CUSTOMERS BY ORDER COUNT",
                 labels={"name": "Customer", "orders_count": "Orders"},
                 color_discrete_sequence=NEON_COLORS)
    apply_chart_style(fig)
    fig.update_layout(xaxis_tickangle=-35)
    st.plotly_chart(fig, use_container_width=True)

# ── CITY MAP ──────────────────────────────────────────────────────────────────
section_header("CUSTOMER DISTRIBUTION BY CITY")

city_data = get_data("/analytics/customers/by-city")
df_city = pd.DataFrame(city_data)
if not df_city.empty:
    col1, col2 = st.columns(2)
    with col1:
        fig = px.pie(df_city, names="city", values="customer_count",
                     title="CUSTOMERS BY CITY", hole=0.45,
                     color_discrete_sequence=NEON_COLORS)
        apply_chart_style(fig)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig2 = px.bar(df_city, x="city", y="customer_count",
                      title="CUSTOMER COUNT PER CITY",
                      color="customer_count",
                      color_continuous_scale=["#050810", "#0033ff", "#00ffc8"],
                      labels={"city": "City", "customer_count": "Customers"})
        apply_chart_style(fig2)
        fig2.update_coloraxes(showscale=False)
        st.plotly_chart(fig2, use_container_width=True)
