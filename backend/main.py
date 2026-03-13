
"""
FastAPI app entry point.
Registers routes and enables CORS for Streamlit.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import customer_analysis, product_analysis, sales_analysis, order_analysis
from .database import get_connection


app = FastAPI(title="Customer Sales Analytics System")

# Allow Streamlit (default port 8501) to call this API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# status ok check endpoint
@app.get("/statusok")
def statusok():
    """
    Simple status ok check; verifies DB connectivity.
    """
    connection = get_connection()
    connection.close()
    return {"status": "ok"}


# Register routers
app.include_router(customer_analysis.router)
app.include_router(product_analysis.router)
app.include_router(sales_analysis.router)
app.include_router(order_analysis.router)
