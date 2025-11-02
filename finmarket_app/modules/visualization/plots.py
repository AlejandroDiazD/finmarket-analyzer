import plotly.graph_objects as go
import pandas as pd
import numpy as np

def plot_candlestick(data: pd.DataFrame, ticker: str):
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
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data["RSI"],
                             name="RSI", line=dict(color='purple')))
    fig.update_layout(yaxis_title="RSI", xaxis_title="Date")
    return fig

def _flatten_and_get_close(df: pd.DataFrame) -> pd.Series:
    """Ensure df has flat columns and return 1D numeric Close series."""
    if isinstance(df.columns, pd.MultiIndex):
        df = df.copy()
        df.columns = [c[0] if isinstance(c, tuple) else c for c in df.columns]
    close = df["Close"]
    if isinstance(close, pd.DataFrame):
        close = close.squeeze()
    close = pd.to_numeric(close, errors="coerce")
    close = close.dropna()
    close = close.sort_index()
    return close

def _y_range_with_padding(series_list, min_pad_ratio: float = 0.01):
    """Compute a y-axis range with a bit of padding so lines are visible."""
    vals = np.concatenate([s.values for s in series_list if s is not None and len(s) > 0])
    if vals.size == 0:
        return None
    y_min, y_max = float(np.nanmin(vals)), float(np.nanmax(vals))
    if not np.isfinite(y_min) or not np.isfinite(y_max):
        return None
    span = max(y_max - y_min, 1e-6)
    pad = max(span * min_pad_ratio, 1e-3)
    return [y_min - pad, y_max + pad]

def plot_forecast(history: pd.DataFrame, forecast: pd.DataFrame, ticker: str):
    """
    Plots historical Close plus forecast yhat with confidence bands.
    Robust to MultiIndex columns and (n,1) frames.
    """
    hist_close = _flatten_and_get_close(history)

    # Build figure
    fig = go.Figure()

    # Historical line
    if len(hist_close) > 0:
        fig.add_trace(go.Scatter(
            x=hist_close.index, y=hist_close,
            name="Historical Close", mode="lines"
        ))

    # Forecast (future) lines
    fc_y = fc_low = fc_up = None
    if forecast is not None and not forecast.empty:
        forecast = forecast.copy()
        # Ensure numeric and sorted
        for col in ["yhat", "yhat_lower", "yhat_upper"]:
            if col in forecast:
                forecast[col] = pd.to_numeric(forecast[col], errors="coerce")
        forecast = forecast.dropna(subset=["yhat"])
        forecast = forecast.sort_index()

        if not forecast.empty:
            fc_y = forecast["yhat"]
            fc_low = forecast["yhat_lower"] if "yhat_lower" in forecast else None
            fc_up  = forecast["yhat_upper"] if "yhat_upper" in forecast else None

            # Confidence band
            if fc_low is not None and fc_up is not None:
                fig.add_trace(go.Scatter(
                    x=list(forecast.index) + list(forecast.index[::-1]),
                    y=list(fc_up.values) + list(fc_low.values[::-1]),
                    fill="toself",
                    fillcolor="rgba(0,0,0,0.08)",
                    line=dict(color="rgba(0,0,0,0)"),
                    hoverinfo="skip",
                    name="Confidence Band"
                ))

            # Forecast line
            fig.add_trace(go.Scatter(
                x=forecast.index, y=fc_y,
                name="Forecast", mode="lines"
            ))

    # Set axis titles and range
    fig.update_layout(
        title=f"{ticker} - Forecast",
        xaxis_title="Date",
        yaxis_title="Price",
        xaxis_rangeslider_visible=False
    )

    # Auto y-range with padding so small slopes are visible
    y_range = _y_range_with_padding([hist_close, fc_y] if fc_y is not None else [hist_close])
    if y_range is not None:
        fig.update_yaxes(range=y_range)

    return fig