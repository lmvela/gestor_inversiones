def generate_signal(latest_price: float, moving_avg: float) -> str:
    if latest_price > moving_avg:
        return "BUY"
    elif latest_price < moving_avg:
        return "SELL"
    return "HOLD"
