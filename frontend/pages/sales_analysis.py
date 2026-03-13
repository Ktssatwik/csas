# """
# Sales analytics page.
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


# st.title("Sales Analysis")


# st.subheader("revenue per Month")
# data = get_data("/analytics/sales/monthly-trend")
# df = pd.DataFrame(data)
# if not df.empty:
#     fig = px.line(df, x="month", y="total_revenue", markers=True)
#     st.plotly_chart(fig, use_container_width=True)
#     st.dataframe(df, use_container_width=True)


# st.subheader("Orders per Month")
# data = get_data("/analytics/sales/orders-per-month")
# df = pd.DataFrame(data)
# if not df.empty:
#     fig = px.bar(df, x="month", y="orders_count", title="Orders per Month")
#     st.plotly_chart(fig, use_container_width=True)
#     st.dataframe(df, use_container_width=True)


# st.subheader("Revenue by City")
# data = get_data("/analytics/sales/revenue-by-city")
# df = pd.DataFrame(data)
# if not df.empty:
#     fig = px.bar(df, x="city", y="total_revenue", title="Revenue by City",color="city")
#     st.plotly_chart(fig, use_container_width=True)
#     st.dataframe(df, use_container_width=True)


# st.subheader("Order Status Breakdown")
# data = get_data("/analytics/sales/status-breakdown")
# df = pd.DataFrame(data)
# if not df.empty:
#     fig = px.pie(df, names="status", values="orders_count", title="Order Status Breakdown")
#     st.plotly_chart(fig, use_container_width=True)
#     st.dataframe(df, use_container_width=True)



"""
CSAS — Sales Analytics Page
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

st.set_page_config(page_title="CSAS // Sales", page_icon="◈", layout="wide")
apply_global_styles()
sidebar_nav()

page_header("SALES ANALYTICS", "TRENDS · GROWTH · GEOGRAPHY · TIMING", "#cc00ff")

# ── KPIs ──────────────────────────────────────────────────────────────────────
section_header("SALES SNAPSHOT")

monthly = get_data("/analytics/sales/monthly-trend")
growth  = get_data("/analytics/sales/monthly-growth")
city_r  = get_data("/analytics/sales/revenue-by-city")
status  = get_data("/analytics/sales/status-breakdown")

df_monthly = pd.DataFrame(monthly)
df_growth  = pd.DataFrame(growth)
df_city    = pd.DataFrame(city_r)
df_status  = pd.DataFrame(status)

total_rev    = df_monthly["total_revenue"].sum() if not df_monthly.empty else 0
latest_month = df_monthly.iloc[-1]["month"] if not df_monthly.empty else "—"
latest_rev   = df_monthly.iloc[-1]["total_revenue"] if not df_monthly.empty else 0
latest_growth = df_growth.iloc[-1]["growth_pct"] if not df_growth.empty else None

k1, k2, k3, k4 = st.columns(4)
k1.metric("TOTAL REVENUE", f"${total_rev:,.0f}")
k2.metric("LATEST MONTH", latest_month)
k3.metric("LATEST MONTH REVENUE", f"${latest_rev:,.0f}")
if latest_growth is not None:
    arrow = "▲" if latest_growth > 0 else "▼"
    color_label = f"{arrow} {abs(latest_growth):.1f}% MoM"
    k4.metric("MoM GROWTH", color_label)
else:
    k4.metric("MoM GROWTH", "—")

st.markdown("<br>", unsafe_allow_html=True)

# ── REVENUE TREND + GROWTH ────────────────────────────────────────────────────
section_header("REVENUE TREND & MONTH-OVER-MONTH GROWTH")

if not df_monthly.empty and not df_growth.empty:
    fig = go.Figure()
    # Revenue area
    fig.add_trace(go.Scatter(
        x=df_monthly["month"], y=df_monthly["total_revenue"],
        fill="tozeroy",
        fillcolor="rgba(204,0,255,0.08)",
        line=dict(color="#cc00ff", width=2.5),
        name="Revenue ($)",
        mode="lines+markers",
        marker=dict(size=6, color="#cc00ff",
                    line=dict(width=1, color="rgba(255,255,255,0.3)")),
    ))
    apply_chart_style(fig)
    fig.update_layout(title="MONTHLY REVENUE TREND", height=340)
    st.plotly_chart(fig, use_container_width=True)

    # Growth % bar
    df_growth_clean = df_growth.dropna(subset=["growth_pct"])
    if not df_growth_clean.empty:
        colors = ["#00ffc8" if v >= 0 else "#ff4060"
                  for v in df_growth_clean["growth_pct"]]
        fig2 = go.Figure(go.Bar(
            x=df_growth_clean["month"],
            y=df_growth_clean["growth_pct"],
            marker_color=colors,
            name="MoM Growth %",
        ))
        fig2.add_hline(y=0, line_dash="dash",
                       line_color="rgba(200,216,240,0.2)", line_width=1)
        apply_chart_style(fig2)
        fig2.update_layout(title="MONTH-OVER-MONTH REVENUE GROWTH (%)", height=280)
        st.plotly_chart(fig2, use_container_width=True)

        pos_months = (df_growth_clean["growth_pct"] > 0).sum()
        insight(f"{pos_months} out of {len(df_growth_clean)} months showed positive growth. Highest: {df_growth_clean['growth_pct'].max():.1f}%, Lowest: {df_growth_clean['growth_pct'].min():.1f}%.")

# ── ORDERS PER MONTH ──────────────────────────────────────────────────────────
section_header("ORDER VOLUME TREND")

orders_month = get_data("/analytics/sales/orders-per-month")
df_opm = pd.DataFrame(orders_month)
if not df_opm.empty:
    fig = px.bar(df_opm, x="month", y="orders_count",
                 title="ORDERS PER MONTH",
                 labels={"month": "Month", "orders_count": "Orders"},
                 color="orders_count",
                 color_continuous_scale=["#050810", "#0033aa", "#0099ff"])
    apply_chart_style(fig)
    fig.update_coloraxes(showscale=False)
    st.plotly_chart(fig, use_container_width=True)

# ── WEEKDAY PATTERNS ──────────────────────────────────────────────────────────
section_header("REVENUE BY DAY OF WEEK")

weekday = get_data("/analytics/sales/revenue-by-weekday")
df_wd = pd.DataFrame(weekday)
if not df_wd.empty:
    df_wd = df_wd.sort_values("day_num")
    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(df_wd, x="weekday", y="total_revenue",
                     title="REVENUE BY WEEKDAY",
                     color="total_revenue",
                     color_continuous_scale=["#050810", "#7b2fff", "#cc00ff"],
                     labels={"weekday": "", "total_revenue": "Revenue ($)"})
        apply_chart_style(fig)
        fig.update_coloraxes(showscale=False)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig2 = px.bar(df_wd, x="weekday", y="orders_count",
                      title="ORDERS BY WEEKDAY",
                      color="orders_count",
                      color_continuous_scale=["#050810", "#7b2fff", "#cc00ff"],
                      labels={"weekday": "", "orders_count": "Orders"})
        apply_chart_style(fig2)
        fig2.update_coloraxes(showscale=False)
        st.plotly_chart(fig2, use_container_width=True)

    best_day = df_wd.loc[df_wd["total_revenue"].idxmax(), "weekday"]
    insight(f"{best_day} drives the most revenue. Consider flash promotions on slower days to smooth out demand.")

# ── CITY × CATEGORY HEATMAP ───────────────────────────────────────────────────
section_header("CITY × CATEGORY REVENUE HEATMAP")

heatmap_data = get_data("/analytics/sales/city-category-heatmap")
df_heat = pd.DataFrame(heatmap_data)
if not df_heat.empty:
    pivot = df_heat.pivot_table(index="city", columns="category",
                                values="total_revenue", fill_value=0)
    fig = go.Figure(go.Heatmap(
        z=pivot.values.tolist(),
        x=pivot.columns.tolist(),
        y=pivot.index.tolist(),
        colorscale=[
            [0.0, "#050810"],
            [0.3, "#0033aa"],
            [0.6, "#cc00ff"],
            [1.0, "#00ffc8"],
        ],
        hoverongaps=False,
        hovertemplate="City: %{y}<br>Category: %{x}<br>Revenue: $%{z:,.0f}<extra></extra>",
    ))
    apply_chart_style(fig)
    fig.update_layout(
        title="REVENUE HEATMAP: CITY × CATEGORY",
        height=420,
        xaxis=dict(tickangle=-20),
    )
    st.plotly_chart(fig, use_container_width=True)
    insight("Identify white-space opportunities: dark cells = untapped city-category combinations worth targeting.")

# ── CITY REVENUE ──────────────────────────────────────────────────────────────
section_header("REVENUE BY CITY")

if not df_city.empty:
    col1, col2 = st.columns([2, 1])
    with col1:
        fig = px.bar(df_city, x="city", y="total_revenue",
                     title="REVENUE BY CITY",
                     color="total_revenue",
                     color_continuous_scale=["#050810", "#0033ff", "#0099ff", "#00ffc8"],
                     labels={"city": "City", "total_revenue": "Revenue ($)"})
        apply_chart_style(fig)
        fig.update_coloraxes(showscale=False)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig2 = px.pie(df_city, names="city", values="total_revenue",
                      title="CITY SHARE", hole=0.4,
                      color_discrete_sequence=NEON_COLORS)
        apply_chart_style(fig2)
        st.plotly_chart(fig2, use_container_width=True)

# ── STATUS BREAKDOWN ──────────────────────────────────────────────────────────
section_header("ORDER STATUS BREAKDOWN")

if not df_status.empty:
    col1, col2 = st.columns(2)
    with col1:
        fig = px.pie(df_status, names="status", values="orders_count",
                     title="ORDER STATUS DISTRIBUTION", hole=0.5,
                     color_discrete_sequence=["#00ffc8", "#0099ff", "#ff4060", "#ffb400", "#cc00ff"])
        apply_chart_style(fig)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig2 = px.bar(df_status, x="status", y="percentage_of_total",
                      title="STATUS % OF TOTAL",
                      color="status",
                      color_discrete_sequence=["#00ffc8", "#0099ff", "#ff4060", "#ffb400", "#cc00ff"],
                      labels={"status": "Status", "percentage_of_total": "% of Orders"})
        apply_chart_style(fig2)
        fig2.update_layout(showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)
