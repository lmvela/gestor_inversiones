from sqlalchemy.orm import Session
from app.models.stock import DailyPrice, IntradayPrice
from statistics import mean

def calculate_moving_average_daily(db: Session, symbol: str, days: int = 5) -> float:
    prices = db.query(DailyPrice).filter(DailyPrice.stock_symbol == symbol).order_by(DailyPrice.date.desc()).limit(days).all()
    return mean([p.close for p in prices]) if prices else None

def calculate_moving_average_intraday(db: Session, symbol: str, days: int = 5) -> float:
    prices = db.query(IntradayPrice).filter(IntradayPrice.stock_symbol == symbol).order_by(IntradayPrice.timestamp.desc()).limit(days).all()
    return mean([p.price for p in prices]) if prices else None
