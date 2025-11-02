from __future__ import annotations
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

def _infer_horizon(interval: str, default: int = 14) -> int:
    return default

def _ensure_series(close: pd.Series | pd.DataFrame) -> pd.Series:
    if isinstance(close, pd.DataFrame):
        close = close.squeeze()
    return close

def make_linear_forecast(
    data: pd.DataFrame,
    interval: str = "1d",
    window: int | None = None,
    horizon: int | None = None
) -> pd.DataFrame:
    """
    Build a simple univariate linear-regression forecast on the Close price.

    - Uses the last `window` points to fit a linear trend.
    - Projects the next `horizon` steps.
    - Adds naive confidence bands from residual std (not statistically rigorous).

    Returns
    -------
    pd.DataFrame
        Forecast DataFrame with index = forecast dates and columns:
        ['yhat', 'yhat_lower', 'yhat_upper']
    """
    if data is None or data.empty:
        return pd.DataFrame()

    close = _ensure_series(data["Close"]).dropna()
    if close.empty or len(close) < 10:
        return pd.DataFrame()

    n = len(close)
    if window is None:
        window = max(30, int(n * 0.5))  # use half the series or at least 30
    window = min(window, n)

    if horizon is None:
        horizon = _infer_horizon(interval, default=14)

    # --- Prepare training data ---
    y = close.iloc[-window:].values  # shape (window,)
    X = np.arange(window).reshape(-1, 1)

    # --- Fit linear model ---
    model = LinearRegression()
    model.fit(X, y)

    # --- Compute in-sample residuals ---
    y_hat_in = model.predict(X)
    resid = y - y_hat_in
    sigma = np.std(resid) if len(resid) > 1 else 0.0

    # --- Predict future ---
    X_fut = np.arange(window, window + horizon).reshape(-1, 1)
    y_hat = model.predict(X_fut)

    # --- Confidence bands (approx. ±1.96σ) ---
    y_lower = y_hat - 1.96 * sigma
    y_upper = y_hat + 1.96 * sigma

    # --- Build future index ---
    last_ts = close.index[-1]
    if close.index.inferred_type in ("datetime64", "datetime64tz"):
        freq_map = {"1d": "D", "1wk": "W", "1mo": "MS"}
        freq = freq_map.get(interval, "D")
        future_index = pd.date_range(last_ts, periods=horizon + 1, freq=freq)[1:]
    else:
        future_index = pd.RangeIndex(n, n + horizon)

    # --- Build output DataFrame ---
    out = pd.DataFrame(
        {"yhat": y_hat, "yhat_lower": y_lower, "yhat_upper": y_upper},
        index=future_index
    )

    # ✅ Clean and sort output (robustness)
    out = out.sort_index()
    out = out.apply(pd.to_numeric, errors="coerce")
    out = out.dropna(subset=["yhat"])

    return out
