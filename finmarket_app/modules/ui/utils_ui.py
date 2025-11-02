def format_asset_title(asset_name: str, ticker: str) -> str:
    """
    Returns a clean and consistent display title for charts and sections.
    Example: "Gold (GC=F)" or "Bitcoin (BTC-USD)".
    """
    if not asset_name or not ticker:
        return asset_name or ticker or "Unknown Asset"
    return f"{asset_name} ({ticker})"
