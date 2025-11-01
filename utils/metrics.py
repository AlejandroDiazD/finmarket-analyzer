import pandas as pd

def get_quick_metrics(data):
    """
    Returns quick metrics: current price, 1-week change, and current RSI.
    """
    current_price = data['Close'].iloc[-1]
    change_week = (data['Close'].iloc[-1] / data['Close'].iloc[-5] - 1) * 100
    current_rsi = data['RSI'].iloc[-1]
    return current_price, change_week, current_rsi
