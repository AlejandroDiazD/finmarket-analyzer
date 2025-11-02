import ta
import pandas as pd

def add_technical_indicators(data: pd.DataFrame) -> pd.DataFrame:
    """
    Adds simple moving averages (SMA 20, SMA 50) and RSI.
    Handles MultiIndex columns from yfinance.
    """
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = [col[0] for col in data.columns]
    if isinstance(data["Close"], pd.DataFrame):
        data["Close"] = data["Close"].squeeze()

    data["SMA_20"] = ta.trend.sma_indicator(data["Close"], window=20)
    data["SMA_50"] = ta.trend.sma_indicator(data["Close"], window=50)
    data["RSI"] = ta.momentum.rsi(data["Close"], window=14)
    return data

