from modules.data.data_loader import load_data
from modules.analysis.forecast import make_linear_forecast

data = load_data("AAPL", "1y", "1d")
fc = make_linear_forecast(data, interval="1d", window=120, horizon=14)
print(fc.head())
