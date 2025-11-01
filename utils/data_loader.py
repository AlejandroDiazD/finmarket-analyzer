import yfinance as yf
import streamlit as st

@st.cache_data
def load_data(ticker: str, period: str, interval: str):
    """
    Downloads historical market data from Yahoo Finance
    and caches the result to improve performance.
    """
    data = yf.download(ticker, period=period, interval=interval)
    data.dropna(inplace=True)
    return data
