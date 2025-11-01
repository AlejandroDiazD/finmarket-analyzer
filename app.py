import streamlit as st
import pandas as pd

from utils.data_loader import load_data
from utils.indicators import add_technical_indicators
from utils.plots import plot_candlestick, plot_rsi
from utils.metrics import get_quick_metrics

st.set_page_config(page_title="Market Insights Dashboard", layout="wide")
st.title("📊 Market Insights Dashboard")

# --- Sidebar ---
st.sidebar.header("Settings")
ticker = st.sidebar.text_input("Asset symbol (e.g., ^GSPC, AAPL, GC=F, BTC-USD)", "^GSPC")
period = st.sidebar.selectbox("Period", ["1y", "5y", "10y", "max"])
interval = st.sidebar.selectbox("Interval", ["1d", "1wk", "1mo"])

# --- Load data ---
data = load_data(ticker, period, interval)
data = add_technical_indicators(data)

# --- Display plots ---
st.plotly_chart(plot_candlestick(data, ticker), use_container_width=True)
st.subheader("📉 Relative Strength Index (RSI)")
st.plotly_chart(plot_rsi(data), use_container_width=True)

# --- Quick metrics ---
st.subheader("📈 Quick Metrics")
col1, col2, col3 = st.columns(3)
price, change_week, rsi = get_quick_metrics(data)
col1.metric("Current Price", f"{price:.2f}")
col2.metric("1-Week Change", f"{change_week:.2f}%")
col3.metric("Current RSI", f"{rsi:.2f}")
