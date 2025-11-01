import ta
import pandas as pd

def add_technical_indicators(data: pd.DataFrame) -> pd.DataFrame:
    """
    Adds basic technical indicators such as SMA20, SMA50, and RSI.
    Handles potential MultiIndex columns from yfinance.
    """

    # Flatten multi-index columns (e.g. ('Close', '') -> 'Close')
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = [col[0] for col in data.columns]

    # Ensure 'Close' is a pandas Series (1D)
    if isinstance(data["Close"], pd.DataFrame):
        data["Close"] = data["Close"].squeeze()  # converts (n,1) -> (n,)

    # Add indicators
    data["SMA_20"] = ta.trend.sma_indicator(data["Close"], window=20)
    data["SMA_50"] = ta.trend.sma_indicator(data["Close"], window=50)
    data["RSI"] = ta.momentum.rsi(data["Close"], window=14)

    return data
