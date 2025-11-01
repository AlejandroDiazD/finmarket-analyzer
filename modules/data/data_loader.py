import yfinance as yf
import streamlit as st
import pandas as pd

@st.cache_data
def load_data(ticker: str, period: str, interval: str) -> pd.DataFrame:
    """
    Downloads market data from Yahoo Finance and caches the result.
    """
    data = yf.download(ticker, period=period, interval=interval, auto_adjust=False)
    if data is None or data.empty:
        st.warning(f"No data found for symbol: {ticker}")
        return pd.DataFrame()
    data.dropna(inplace=True)
    return data
