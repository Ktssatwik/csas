"""
Shared utilities for CSAS Streamlit pages.
Import this at the top of every page file.
"""

import os
import requests
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from dotenv import load_dotenv

load_dotenv()
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

NEON_COLORS = ["#00ffc8", "#0099ff", "#cc00ff", "#ffb400", "#ff4060",
               "#00e5ff", "#7b2fff", "#ff6e00"]


def apply_global_styles():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700;900&family=Share+Tech+Mono&family=Rajdhani:wght@300;400;600&display=swap');

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
[data-testid="stSidebarNav"] { display: none; }

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
}
.stButton > button:hover {
    background: rgba(0,255,200,0.08) !important;
    border-color: #00ffc8 !important;
    box-shadow: 0 0 20px rgba(0,255,200,0.25), inset 0 0 20px rgba(0,255,200,0.05) !important;
    color: #ffffff !important;
}

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
    font-size: 26px !important;
    font-weight: 700 !important;
}

[data-testid="stDataFrame"] {
    border: 1px solid rgba(0,255,200,0.12) !important;
    border-radius: 4px !important;
}
hr { border-color: rgba(0,255,200,0.1) !important; }

::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: #050810; }
::-webkit-scrollbar-thumb { background: rgba(0,255,200,0.3); border-radius: 2px; }

[data-testid="stSelectbox"] > div > div {
    background: rgba(0,255,200,0.05) !important;
    border: 1px solid rgba(0,255,200,0.25) !important;
    color: #c8d8f0 !important;
    font-family: 'Share Tech Mono', monospace !important;
    border-radius: 2px !important;
}

.section-header {
    font-family: 'Orbitron', monospace;
    font-size: 13px;
    font-weight: 700;
    color: #00ffc8;
    letter-spacing: 3px;
    text-transform: uppercase;
    padding: 20px 0 8px;
    border-bottom: 1px solid rgba(0,255,200,0.15);
    margin-bottom: 16px;
}
.insight-box {
    background: linear-gradient(135deg, rgba(0,255,200,0.05), rgba(0,140,255,0.03));
    border: 1px solid rgba(0,255,200,0.18);
    border-left: 3px solid #00ffc8;
    border-radius: 0 4px 4px 0;
    padding: 12px 16px;
    margin: 8px 0;
    font-family: 'Rajdhani', sans-serif;
    font-size: 14px;
    color: rgba(200,216,240,0.8);
}
</style>
""", unsafe_allow_html=True)


def page_header(title: str, subtitle: str = "", accent: str = "#00ffc8"):
    st.markdown(f"""
<div style='padding: 24px 0 16px;'>
    <div style='font-family: Share Tech Mono, monospace; font-size: 10px;
                color: rgba(0,255,200,0.4); letter-spacing: 4px;
                text-transform: uppercase; margin-bottom: 6px;'>
        ◈ CSAS // MODULE
    </div>
    <div style='font-family: Orbitron, monospace; font-size: 32px; font-weight: 900;
                letter-spacing: 3px; text-transform: uppercase;
                color: {accent}; text-shadow: 0 0 30px {accent}55;'>
        {title}
    </div>
    <div style='font-family: Rajdhani, sans-serif; font-size: 14px; font-weight: 300;
                color: rgba(200,216,240,0.45); letter-spacing: 2px;
                text-transform: uppercase; margin-top: 4px;'>
        {subtitle}
    </div>
</div>
""", unsafe_allow_html=True)


def section_header(text: str):
    st.markdown(f"<div class='section-header'>◈ {text}</div>", unsafe_allow_html=True)


def insight(text: str):
    st.markdown(f"<div class='insight-box'>⚡ {text}</div>", unsafe_allow_html=True)


# dis is tha importsnt  
def get_data(path: str):
    url = f"{API_BASE_URL}{path}"
    response = requests.get(url, timeout=30)
    # response = requests.post(url, timeout=30)
    response.raise_for_status()
    return response.json()


def apply_chart_style(fig):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(5,8,16,0.95)",
        font=dict(family="Share Tech Mono, monospace", color="#c8d8f0", size=11),
        title_font=dict(family="Orbitron, monospace", color="#00ffc8", size=13),
        legend=dict(
            bgcolor="rgba(5,8,16,0.8)",
            bordercolor="rgba(0,255,200,0.15)",
            borderwidth=1,
        ),
        xaxis=dict(gridcolor="rgba(0,255,200,0.07)", linecolor="rgba(0,255,200,0.12)"),
        yaxis=dict(gridcolor="rgba(0,255,200,0.07)", linecolor="rgba(0,255,200,0.12)"),
        margin=dict(l=40, r=20, t=45, b=40),
    )
    return fig


def sidebar_nav():
    with st.sidebar:
        st.markdown("""
<div style='text-align:center; padding: 16px 0 8px;'>
    <div style='font-family: Orbitron, monospace; font-size:20px; font-weight:900;
                color:#00ffc8; letter-spacing:2px; text-shadow: 0 0 20px rgba(0,255,200,0.5);'>
        CSAS
    </div>
    <div style='font-family: Share Tech Mono, monospace; font-size:10px;
                color:rgba(200,216,240,0.35); letter-spacing:1px;'>
        ANALYTICS 
    </div>
</div>
""", unsafe_allow_html=True)
        st.markdown("---")
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
        try:
            r = requests.get(f"{API_BASE_URL}/statusok", timeout=3)
            if r.status_code == 200:
                st.markdown("<div style='font-family:Share Tech Mono,monospace;font-size:11px;color:#00ffc8;'>● API ONLINE</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div style='font-family:Share Tech Mono,monospace;font-size:11px;color:#ff4060;'>● API ERROR</div>", unsafe_allow_html=True)
        except Exception:
            st.markdown("<div style='font-family:Share Tech Mono,monospace;font-size:11px;color:#ff8c00;'>● API OFFLINE</div>", unsafe_allow_html=True)
