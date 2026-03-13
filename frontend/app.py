# """
# CSAS Streamlit Landing Page
# Modern UI + Dark Mode Compatible
# """

# import streamlit as st

# st.set_page_config(
#     page_title="CSAS Dashboard",
#     page_icon="📊",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # ---------------- SESSION STATE ----------------

# if "started" not in st.session_state:
#     st.session_state.started = False

# if "selected_section" not in st.session_state:
#     st.session_state.selected_section = None


# # ---------------- DARK MODE FRIENDLY CSS ----------------

# st.markdown("""
# <style>

# /* Main background */

# body{
# background: var(--background-color);
# color: var(--text-color);
# }


# /* Header */

# .title{
# font-size:48px;
# font-weight:800;
# text-align:center;
# background: linear-gradient(90deg,#4f8cff,#00c6ff);
# -webkit-background-clip:text;
# -webkit-text-fill-color:transparent;
# }

# .subtitle{
# text-align:center;
# color: var(--text-color);
# opacity:0.7;
# font-size:18px;
# margin-bottom:25px;
# }


# /* Metric cards */

# .metric-card{
# background: var(--secondary-background-color);
# padding:25px;
# border-radius:16px;
# border:1px solid rgba(128,128,128,0.2);
# transition:0.25s;
# }

# .metric-card:hover{
# transform:translateY(-6px);
# box-shadow:0 10px 30px rgba(0,0,0,0.25);
# }


# /* Analytics cards */

# .analytics-card button{
# height:180px;
# border-radius:16px;
# border:1px solid rgba(128,128,128,0.25);
# background: var(--secondary-background-color);
# color: var(--text-color);
# font-size:16px;
# font-weight:600;
# padding:20px;
# text-align:left;
# transition:0.25s;
# white-space:pre-line;
# }
# .analytics-card button::first-line{
# font-size:22px;
# font-weight:800;
# }

# .analytics-card button:hover{
# transform:translateY(-8px);
# box-shadow:0 10px 35px rgba(0,0,0,0.35);
# border-color: var(--primary-color);
# }


# /* Sidebar */

# section[data-testid="stSidebar"]{
# background: var(--secondary-background-color);
# }

# /* Smaller Get Started button */
# .start-btn .stButton > button{
# height:44px;
# width:auto;
# padding:8px 16px;
# font-size:14px;
# border-radius:10px;
# }

# </style>
# """, unsafe_allow_html=True)


# # ---------------- SIDEBAR ----------------

# st.sidebar.title("📊 CSAS Dashboard")

# st.sidebar.markdown("### Navigation")

# if st.sidebar.button("🏠 Home"):
#     st.session_state.started = True

# if st.sidebar.button("👥 Customer Analytics"):
#     st.switch_page("pages/customer_analysis.py")

# if st.sidebar.button("📦 Product Analytics"):
#     st.switch_page("pages/product_analysis.py")

# if st.sidebar.button("💰 Sales Analytics"):
#     st.switch_page("pages/sales_analysis.py")

# if st.sidebar.button("🧾 Order Analytics"):
#     st.switch_page("pages/order_analysis.py")

# st.sidebar.markdown("---")
# st.sidebar.markdown("Customer Sales Analytics System")


# # ---------------- HEADER ----------------

# st.markdown(
#     '<div class="title">Customer Sales Analytics System</div>',
#     unsafe_allow_html=True
# )

# st.markdown(
#     '<div class="subtitle">Powerful insights for smarter retail decisions</div>',
#     unsafe_allow_html=True
# )


# # ---------------- GET STARTED ----------------

# center = st.columns([1,2,1])

# with center[1]:
#     if st.button("🚀 Get Started", use_container_width=True):
#         st.session_state.started = True

# if not st.session_state.started:
#     st.stop()


# st.markdown("---")


# # ---------------- KPI METRICS ----------------

# st.markdown("### 📈 Quick Insights")

# m1, m2, m3, m4 = st.columns(4)

# with m1:
#     st.markdown("""
#     <div class="metric-card">
#     <h3>👥 Customers</h3>
#     <h2>1,250</h2>
#     <p>Total registered customers</p>
#     </div>
#     """, unsafe_allow_html=True)

# with m2:
#     st.markdown("""
#     <div class="metric-card">
#     <h3>📦 Products</h3>
#     <h2>320</h2>
#     <p>Products available</p>
#     </div>
#     """, unsafe_allow_html=True)

# with m3:
#     st.markdown("""
#     <div class="metric-card">
#     <h3>🧾 Orders</h3>
#     <h2>4,870</h2>
#     <p>Total completed orders</p>
#     </div>
#     """, unsafe_allow_html=True)

# with m4:
#     st.markdown("""
#     <div class="metric-card">
#     <h3>💰 Revenue</h3>
#     <h2>$920K</h2>
#     <p>Total revenue generated</p>
#     </div>
#     """, unsafe_allow_html=True)


# st.markdown("---")


# # ---------------- ANALYTICS MODULES ----------------

# st.markdown("### 🔎 Explore Analytics")

# c1, c2, c3, c4 = st.columns(4)

# with c1:
#     st.markdown('<div class="analytics-card">', unsafe_allow_html=True)
#     if st.button(
#         "👥 Customer Analytics\n\nTop customers\nCity distribution\nPurchase patterns",
#         key="customers",
#     ):
#         st.session_state.selected_section = "customers"
#         st.switch_page("pages/customer_analysis.py")
#     st.markdown('</div>', unsafe_allow_html=True)

# with c2:
#     st.markdown('<div class="analytics-card">', unsafe_allow_html=True)
#     if st.button(
#         "📦 Product Analytics\n\nBest selling products\nCategory insights\nProduct revenue",
#         key="products",
#     ):
#         st.session_state.selected_section = "products"
#         st.switch_page("pages/product_analysis.py")
#     st.markdown('</div>', unsafe_allow_html=True)

# with c3:
#     st.markdown('<div class="analytics-card">', unsafe_allow_html=True)
#     if st.button(
#         "💰 Sales Analytics\n\nMonthly trends\nRevenue analysis\nSales growth",
#         key="sales",
#     ):
#         st.session_state.selected_section = "sales"
#         st.switch_page("pages/sales_analysis.py")
#     st.markdown('</div>', unsafe_allow_html=True)

# with c4:
#     st.markdown('<div class="analytics-card">', unsafe_allow_html=True)
#     if st.button(
#         "🧾 Order Analytics\n\nAverage order value\nItems per order\nOrder insights",
#         key="orders",
#     ):
#         st.session_state.selected_section = "orders"
#         st.switch_page("pages/order_analysis.py")
#     st.markdown('</div>', unsafe_allow_html=True)



"""
CSAS — Customer Sales Analytics System
"""

import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

st.set_page_config(
    page_title="CSAS // Analytics",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── GLOBAL CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700;900&family=Share+Tech+Mono&family=Rajdhani:wght@300;400;600&display=swap');

/* Base */
html, body, [data-testid="stAppViewContainer"] {
    background-color: #050810 !important;
    color: #c8d8f0 !important;
}
[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse at 20% 50%, rgba(0,255,200,0.04) 0%, transparent 60%),
        radial-gradient(ellipse at 80% 20%, rgba(0,140,255,0.05) 0%, transparent 55%),
        radial-gradient(ellipse at 60% 80%, rgba(180,0,255,0.04) 0%, transparent 55%),
        #050810 !important;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #080d1a 0%, #060b16 100%) !important;
    border-right: 1px solid rgba(0,255,200,0.15) !important;
}
[data-testid="stSidebar"] * { font-family: 'Share Tech Mono', monospace !important; }

/* Buttons */
.stButton > button {
    background: transparent !important;
    border: 1px solid rgba(0,255,200,0.4) !important;
    color: #00ffc8 !important;
    font-family: 'Orbitron', monospace !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    border-radius: 2px !important;
    transition: all 0.2s ease !important;
    padding: 8px 18px !important;
}
.stButton > button:hover {
    background: rgba(0,255,200,0.08) !important;
    border-color: #00ffc8 !important;
    box-shadow: 0 0 20px rgba(0,255,200,0.25), inset 0 0 20px rgba(0,255,200,0.05) !important;
    color: #ffffff !important;
}

/* Metric */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, rgba(0,255,200,0.04), rgba(0,140,255,0.04)) !important;
    border: 1px solid rgba(0,255,200,0.18) !important;
    border-radius: 4px !important;
    padding: 16px !important;
}
[data-testid="stMetricLabel"] {
    font-family: 'Share Tech Mono', monospace !important;
    color: rgba(0,255,200,0.7) !important;
    font-size: 11px !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Orbitron', monospace !important;
    color: #ffffff !important;
    font-size: 28px !important;
    font-weight: 700 !important;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border: 1px solid rgba(0,255,200,0.15) !important;
    border-radius: 4px !important;
}

/* Divider */
hr { border-color: rgba(0,255,200,0.12) !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: #050810; }
::-webkit-scrollbar-thumb { background: rgba(0,255,200,0.3); border-radius: 2px; }

/* Select boxes */
[data-testid="stSelectbox"] > div > div {
    background: rgba(0,255,200,0.05) !important;
    border: 1px solid rgba(0,255,200,0.25) !important;
    color: #c8d8f0 !important;
    font-family: 'Share Tech Mono', monospace !important;
    border-radius: 2px !important;
}

/* Plotly charts border */
.js-plotly-plot {
    border: 1px solid rgba(0,255,200,0.1) !important;
    border-radius: 4px !important;
}
</style>
""", unsafe_allow_html=True)

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 20px 0 10px;'>
        <div style='font-family: Orbitron, monospace; font-size:11px; letter-spacing:4px;
                    color:rgba(0,255,200,0.5); text-transform:uppercase;'>System</div>
        <div style='font-family: Orbitron, monospace; font-size:20px; font-weight:900;
                    color:#00ffc8; letter-spacing:2px; text-shadow: 0 0 20px rgba(0,255,200,0.5);'>
            CSAS
        </div>
        <div style='font-family: Share Tech Mono, monospace; font-size:10px;
                    color:rgba(200,216,240,0.4); letter-spacing:1px;'>
            ANALYTICS // v2.0
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<div style='font-family:Share Tech Mono,monospace;font-size:10px;color:rgba(0,255,200,0.5);letter-spacing:2px;padding:8px 0 4px;'>// NAVIGATE</div>", unsafe_allow_html=True)

    if st.button("⬡  HOME", use_container_width=True):
        st.switch_page("app.py")
    if st.button("◈  CUSTOMERS", use_container_width=True):
        st.switch_page("pages/customer_analysis.py")
    if st.button("◈  PRODUCTS", use_container_width=True):
        st.switch_page("pages/product_analysis.py")
    if st.button("◈  SALES", use_container_width=True):
        st.switch_page("pages/sales_analysis.py")
    if st.button("◈  ORDERS", use_container_width=True):
        st.switch_page("pages/order_analysis.py")

    st.markdown("---")

    # Live status check
    try:
        r = requests.get(f"{API_BASE_URL}/statusok", timeout=3)
        if r.status_code == 200:
            st.markdown("<div style='font-family:Share Tech Mono,monospace;font-size:11px;color:#00ffc8;'>● API ONLINE</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div style='font-family:Share Tech Mono,monospace;font-size:11px;color:#ff4060;'>● API ERROR</div>", unsafe_allow_html=True)
    except Exception:
        st.markdown("<div style='font-family:Share Tech Mono,monospace;font-size:11px;color:#ff8c00;'>● API OFFLINE</div>", unsafe_allow_html=True)

# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='padding: 40px 0 10px; text-align:center;'>
    <div style='font-family: Share Tech Mono, monospace; font-size: 11px;
                color: rgba(0,255,200,0.5); letter-spacing: 5px;
                text-transform: uppercase; margin-bottom: 8px;'>
        ◈ CUSTOMER SALES ANALYTICS SYSTEM ◈
    </div>
    <div style='font-family: Orbitron, monospace; font-size: 42px; font-weight: 900;
                letter-spacing: 4px; text-transform: uppercase;
                background: linear-gradient(90deg, #00ffc8, #0099ff, #cc00ff);
                -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                text-shadow: none; line-height: 1.1;'>
        RETAIL INTELLIGENCE
    </div>
    <div style='font-family: Rajdhani, sans-serif; font-size: 16px; font-weight: 300;
                color: rgba(200,216,240,0.5); letter-spacing: 3px;
                text-transform: uppercase; margin-top: 8px;'>
        POWERED BY FASTAPI // MYSQL // STREAMLIT
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── LIVE KPI ROW ──────────────────────────────────────────────────────────────
def safe_get(path):
    try:
        r = requests.get(f"{API_BASE_URL}{path}", timeout=5)
        r.raise_for_status()
        return r.json()
    except Exception:
        return None

col1, col2, col3, col4 = st.columns(4)

avg_val = safe_get("/analytics/orders/average-order-value")
avg_items = safe_get("/analytics/orders/average-items-per-order")
top_city = safe_get("/analytics/sales/revenue-by-city")
repeat = safe_get("/analytics/customers/repeat-vs-new")

with col1:
    val = avg_val.get("avg_order_value", "—") if avg_val else "—"
    st.metric("AVG ORDER VALUE", f"${val}" if val != "—" else "—")

with col2:
    val = avg_items.get("avg_items_per_order", "—") if avg_items else "—"
    st.metric("AVG ITEMS / ORDER", val)

with col3:
    if top_city and len(top_city) > 0:
        st.metric("TOP REVENUE CITY", top_city[0]["city"])
    else:
        st.metric("TOP REVENUE CITY", "—")

with col4:
    if repeat:
        repeat_count = next((x["customer_count"] for x in repeat if x["customer_type"] == "Repeat"), 0)
        new_count = next((x["customer_count"] for x in repeat if x["customer_type"] == "New"), 0)
        total = repeat_count + new_count
        pct = round(repeat_count / total * 100, 1) if total > 0 else 0
        st.metric("REPEAT CUSTOMER RATE", f"{pct}%")
    else:
        st.metric("REPEAT CUSTOMER RATE", "—")

st.markdown("<br>", unsafe_allow_html=True)

# ── MODULE CARDS ──────────────────────────────────────────────────────────────
st.markdown("""
<div style='font-family: Share Tech Mono, monospace; font-size: 11px;
            color: rgba(0,255,200,0.5); letter-spacing: 4px;
            text-transform: uppercase; margin-bottom: 20px;'>
    // SELECT MODULE
</div>
""", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)

CARD = """
<div style='
    background: linear-gradient(135deg, rgba({r},{g},{b},0.08), rgba({r},{g},{b},0.03));
    border: 1px solid rgba({r},{g},{b},0.3);
    border-radius: 4px;
    padding: 24px 20px;
    margin-bottom: 8px;
    min-height: 160px;
'>
    <div style='font-family: Orbitron, monospace; font-size: 22px; color: rgb({r},{g},{b});
                margin-bottom: 6px;'>{icon}</div>
    <div style='font-family: Orbitron, monospace; font-size: 13px; font-weight: 700;
                color: rgb({r},{g},{b}); letter-spacing: 2px; margin-bottom: 10px;
                text-transform: uppercase;'>{title}</div>
    <div style='font-family: Rajdhani, sans-serif; font-size: 13px; font-weight: 300;
                color: rgba(200,216,240,0.6); line-height: 1.6;'>{desc}</div>
</div>
"""

with c1:
    st.markdown(CARD.format(r=0,g=255,b=200, icon="◈", title="CUSTOMERS",
        desc="CLV · Repeat rate<br>Top spenders · City map"), unsafe_allow_html=True)
    if st.button("LAUNCH →", key="cust", use_container_width=True):
        st.switch_page("pages/customer_analysis.py")

with c2:
    st.markdown(CARD.format(r=0,g=153,b=255, icon="◈", title="PRODUCTS",
        desc="Revenue leaders · Price analysis<br>Category heatmap · Laggards"), unsafe_allow_html=True)
    if st.button("LAUNCH →", key="prod", use_container_width=True):
        st.switch_page("pages/product_analysis.py")

with c3:
    st.markdown(CARD.format(r=180,g=0,b=255, icon="◈", title="SALES",
        desc="Growth trends · MoM analysis<br>City revenue · Weekday patterns"), unsafe_allow_html=True)
    if st.button("LAUNCH →", key="sales", use_container_width=True):
        st.switch_page("pages/sales_analysis.py")

with c4:
    st.markdown(CARD.format(r=255,g=180,b=0, icon="◈", title="ORDERS",
        desc="Value tiers · High-value orders<br>Avg value · Items per order"), unsafe_allow_html=True)
    if st.button("LAUNCH →", key="ord", use_container_width=True):
        st.switch_page("pages/order_analysis.py")

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align:center; font-family: Share Tech Mono, monospace;
            font-size: 10px; color: rgba(200,216,240,0.2); letter-spacing: 2px;'>
    CSAS // CUSTOMER SALES ANALYTICS SYSTEM // ALL DATA SERVED VIA FASTAPI
</div>
""", unsafe_allow_html=True)
