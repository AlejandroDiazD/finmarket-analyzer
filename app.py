import streamlit as st
import pandas as pd

from modules.data.data_loader import load_data
from modules.analysis.indicators import add_technical_indicators
from modules.analysis.metrics import get_quick_metrics
from modules.analysis.forecast import make_linear_forecast
from modules.visualization.plots import plot_candlestick, plot_rsi, plot_forecast
from modules.ui.user_guide import render_user_guide

st.set_page_config(page_title="Market Insights Dashboard", layout="wide")
st.title("📊 Market Insights Dashboard")

# --- Sidebar ---
st.sidebar.header("Settings")
# Dropdown for asset selection
asset_options = {
    # ---- Global Indices ----
    "MSCI World": "URTH",
    "MSCI Emerging Markets": "EEM",

    # ---- Commodities ----
    "Gold": "GC=F",

    # ---- Cryptocurrencies ----
    "Bitcoin": "BTC-USD",
    "Ethereum": "ETH-USD",

    # ---- Fixed Income ----
    "EU Gov Bonds 1-3Y": "IBGX.DE",

    # ---- Thematic ETFs ----
    "VanEck Uranium & Nuclear ETF": "NLR",
    "iShares Global Clean Energy": "ICLN",
}

asset_name = st.sidebar.selectbox("Select asset", list(asset_options.keys()))
ticker = asset_options[asset_name]

period = st.sidebar.selectbox("Period", ["1y", "5y", "10y", "max"])
interval = st.sidebar.selectbox("Interval", ["1d", "1wk", "1mo"])

st.sidebar.header("Forecast Settings")
forecast_horizon = st.sidebar.slider("Horizon (steps)", 7, 90, 14)
forecast_window = st.sidebar.slider("Training window (points)", 30, 365, 120)

# --- Tabs ---
tab_dashboard, tab_forecast, tab_guide = st.tabs(["📈 Dashboard", "🔮 Forecast", "📘 User Guide"])

with tab_dashboard:
    data = load_data(ticker, period, interval)
    if data.empty:
        st.error("⚠️ No market data available for this ticker.")
        st.stop()

    data = add_technical_indicators(data)
    st.plotly_chart(plot_candlestick(data, f"{asset_name} ({ticker})"), width='stretch')
    st.subheader("📉 Relative Strength Index (RSI)")
    st.plotly_chart(plot_rsi(data), width='stretch')

    st.subheader("📈 Quick Metrics")
    col1, col2, col3 = st.columns(3)
    price, change_week, rsi = get_quick_metrics(data)
    col1.metric("Current Price", f"{price:.2f}")
    col2.metric("1-Week Change", f"{change_week:.2f}%")
    col3.metric("Current RSI", f"{rsi:.2f}")

with tab_forecast:
    st.subheader("🔮 Simple Linear Forecast")
    data = load_data(ticker, period, interval)
    if data.empty:
        st.warning("No data available to build a forecast.")
        st.stop()

    fc = make_linear_forecast(data, interval, forecast_window, forecast_horizon)
    if fc.empty:
        st.warning("Not enough data to produce a forecast.")
    else:
        st.plotly_chart(plot_forecast(data, fc, f"{asset_name} ({ticker})"), width='stretch')

    st.info("This forecast uses a simple linear regression trend based on recent data.")

with tab_guide:
    render_user_guide()
