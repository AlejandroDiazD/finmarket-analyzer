import pandas as pd

def get_quick_metrics(data: pd.DataFrame):
    """
    Returns quick metrics: current price, 1-week change, and current RSI.
    """
    current_price = data['Close'][-1]
    change_week = (data['Close'][-1] / data['Close'][-5] - 1) * 100
    current_rsi = data['RSI'][-1]
    return current_price, change_week, current_rsi
