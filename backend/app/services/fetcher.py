import yfinance as yf

def fetch_stock_price(symbol: str) -> float:
    ticker = yf.Ticker(symbol)
    data = ticker.history(period="1d")
    return data["Close"].iloc[-1] if not data.empty else None
