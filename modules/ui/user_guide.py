import streamlit as st

def render_user_guide():
    """
    Renders the User Guide tab explaining how to interpret and use the dashboard.
    """
    st.header("📘 How to Use the Dashboard")

    st.markdown("""
    ### 🎯 Purpose
    This dashboard lets you explore and analyze financial market data interactively.

    ### 🧭 Main Controls
    - **Asset symbol:** Choose any market ticker (e.g., `^GSPC`, `AAPL`, `GC=F`, `BTC-USD`).
    - **Period:** Time range for historical data.
    - **Interval:** Data granularity (daily, weekly, or monthly).

    ### 📊 Charts
    - **Candlestick chart:** Displays open, high, low, and close prices.
    - **SMA 20 & SMA 50:** Moving averages to detect short- and mid-term trends.
    - **RSI (Relative Strength Index):**
      - Above 70 → Overbought
      - Below 30 → Oversold

    ### 📈 Quick Metrics
    - **Current Price:** Latest closing price.
    - **1-Week Change:** Percentage change compared to one week ago.
    - **Current RSI:** Indicates whether the market is strong or weak.

    ### 💡 Tips
    - Combine RSI with SMA crossovers for stronger insights.
    - Use different periods to compare short vs long-term trends.
    """)
    st.info("This section is optional — open it anytime to recall how to interpret the dashboard.")
