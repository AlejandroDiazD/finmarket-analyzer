import plotly.graph_objects as go
import pandas as pd

def plot_candlestick(data: pd.DataFrame, ticker: str):
    """
    Creates a candlestick chart with SMA20 and SMA50 overlays.
    """
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=data.index,
        open=data['Open'], high=data['High'],
        low=data['Low'], close=data['Close'],
        name='Price'
    ))
    fig.add_trace(go.Scatter(x=data.index, y=data['SMA_20'],
                             line=dict(color='orange', width=1.5),
                             name='SMA 20'))
    fig.add_trace(go.Scatter(x=data.index, y=data['SMA_50'],
                             line=dict(color='blue', width=1.5),
                             name='SMA 50'))

    fig.update_layout(title=f"{ticker} - Price and Indicators",
                      xaxis_rangeslider_visible=False)
    return fig


def plot_rsi(data: pd.DataFrame):
    """
    Creates a line chart for the RSI indicator.
    """
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data["RSI"], name="RSI", line=dict(color='purple')))
    fig.update_layout(yaxis_title="RSI", xaxis_title="Date")
    return fig
